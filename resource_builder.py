import os
import sys
from pathlib import Path
from typing import List

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

import audio_metadata
from mp3hash import mp3hash
from PIL import Image
from lxml import etree as et
from uuid import uuid4 as uuid
from enum import Enum

#  local imports
from pydex.utils import (add_subelement_with_text, 
                         get_logger, 
                         format_duration,
                         compute_image_hash)
from pydex.config import LOG_DIR, TEST_XML_DIR, FIXTURES_DIR
from pydex.tags import (ResourceListTags, 
                        SoundRecordingTags, 
                        TechnicalDetailsType,
                        TechnicalDetailsTags,
                        ImageType,
                        ImageTags)
from pydex.exceptions import (
        MissingAttribute,
        InvalidTypeError,
        )

logger = get_logger(__name__, 'ddex')


class ResourceList:
    """
    Builds ResourceList tag
    """

    def __init__(self, sound_recording: list, image: et.Element):
        if isinstance(sound_recording, list):
            logger.debug(f'Creating ResourceList with {len(sound_recording)} sound recordings')
            self.sound_recording = sound_recording
        else:
            # TODO: need to test raising TypeError
            logger.error(f'Expected list, got {type(sound_recording)}')
            raise TypeError('sound_recording must be of type list')
        self.image = image

    def write(self):
        logger.info("Building ResourceList tag.")
        tag: et.Element = et.Element(ResourceListTags.root.value)
        for sound_recording in self.sound_recording:
            tag.append(sound_recording.write())
        tag.append(self.image.write())
        return tag


class TechnicalDetails:
    def __init__(self,
                 type_: Enum,
                 file: str,
                 resource_uuid: str,
                 **kwargs
                 ):
        self.type = type_
        self.file = file
        self.resource_uuid = resource_uuid

        if type_ == TechnicalDetailsType.audio.value:
            logger.debug('Initializing TechnicalDetails of Audio Type')
            self.audio_data = audio_metadata.load(file)
            logger.debug(f'Loaded audio_data from {self.file}')
            self.metadata = self.audio_data['streaminfo']
            logger.debug('Loaded audio_metadata.')
            self.audio_codec = self.audio_data.filepath.split('.')[-1]
            logger.debug(f'Found audio codec from file: {self.audio_codec}')
            self.bitrate = str(self.metadata.bitrate / 1000)
            logger.debug(f"Found bitrate to be {self.bitrate}")
            self.channels = str(self.metadata.channels)
            logger.debug(f"Found channels to be {self.channels}")
            self.sample_rate = str(self.metadata.sample_rate / 1000)
            logger.debug(f"Found sample_rate to be {self.sample_rate}")
            logger.debug(f"Sending duration {self.metadata.duration} to be formatted.")
            self.duration = format_duration(self.metadata.duration)
            logger.debug(f"Found formatted duration to be {self.duration}")
            try:
                self.hash_value = mp3hash(file)
            except TypeError:
                logger.error('Got TypeError mp3hash might not be imported correctly.')
            logger.debug(f"Computed hash of the file {self.hash_value}.")

            #  Check if audio_codec value is WAV
            if self.audio_codec == 'wav':
                if kwargs.get('sender_id'):
                    self.sender_id = kwargs.get('sender_id')
                else:
                    logger.error(f"sender_id was not provided for filetype {self.audio_codec}")
                    raise MissingAttribute(self.audio_codec)

        if type_ == TechnicalDetailsType.image.value:
            logger.debug('Initializing TechnicalDetails of Image Type.')
            self.image = Image.open(file)


    def get_reference(self):
        logger.debug('Building technical resource reference id.')
        return f"T{self.resource_uuid}"

    def build_hash_sum(self):
        tag = et.Element(TechnicalDetailsTags.hash_sum.value)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.algorithm.value,
                                 "MD5")
        if self.type == TechnicalDetailsType.audio.value:
            add_subelement_with_text(tag,
                                    TechnicalDetailsTags.hash_sum_value.value,
                                    self.hash_value)
        if self.type == TechnicalDetailsType.image.value:
            hash_value = compute_image_hash(self.file)
            add_subelement_with_text(tag,
                                     TechnicalDetailsTags.hash_sum_value.value,
                                     hash_value)
        return tag

    def build_file(self):
        logger.debug(f"Building file for type {self.type}")
        tag = et.Element(TechnicalDetailsTags.file.value)
        add_subelement_with_text(tag,
                                TechnicalDetailsTags.uri.value,
                                self.file)
        tag.append(self.build_hash_sum())
        return tag

    def build_audio_technical_details(self):
        logger.info('Building technical details for Audio type.')
        tag = et.Element(TechnicalDetailsTags.root.value)
        logger.debug('Got root ready.')
        add_subelement_with_text(tag, 
                                 TechnicalDetailsTags.details_reference.value,
                                 self.get_reference())
        if self.file.endswith('wav'):
            add_subelement_with_text(tag,
                                     TechnicalDetailsTags.audio_codec.value,
                                     'UserDefined', 
                                     UserDefinedValue='WAV',
                                     Namespace=self.sender_id)
        else:
            add_subelement_with_text(tag,
                                     TechnicalDetailsTags.audio_codec.value,
                                     self.audio_codec)

        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.channels.value,
                                 self.channels)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.sample_rate.value,
                                 self.sample_rate)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.bitrate.value,
                                 self.bitrate)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.duration.value,
                                 self.duration)
        tag.append(self.build_file())
        return tag

    def build_image_technical_details(self):
        tag = et.Element(TechnicalDetailsType.image.value)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.details_reference.value,
                                 self.resource_uuid)
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.image_height.value,
                                 str(self.image.height))
        add_subelement_with_text(tag,
                                 TechnicalDetailsTags.image_width.value,
                                 str(self.image.width))
        tag.append(self.build_file())
        return tag


    def write(self):
        logger.debug("Inside write function.")
        logger.debug(f"Type: {self.type}")
        if self.type == TechnicalDetailsType.audio.value:
            logger.debug("Building audio type TechnicalDetails")
            return self.build_audio_technical_details()
        if self.type == TechnicalDetailsType.image.value:
            logger.debug("Building image type TechnicalDetails")
            return self.build_image_technical_details()



class SoundRecording:
    """
    Builds SoundRecording tag
    """

    def __init__(
            self,
            type_: str,
            id_: str,
            song_name: str,
            artist_name: str,
            pline_text: str,
            parental_warning_type: str,
            technical_details: et.Element,
            party: List[et.Element],
            contributor: List[et.Element],
            pline_company=None,
            pline_year=None,
    ):
        self.type = type_
        self.id = id_
        self.song_name = song_name
        self.artist_name = artist_name
        self.pline_text = pline_text
        self.parental_warning_type = parental_warning_type
        self.technical_details = technical_details
        self.party = party
        self.contributor = contributor
        self.pline_company = pline_company
        self.pline_year = pline_year

    @staticmethod
    def get_reference():
        """
        Return a uuid4 string
        """
        logger.debug('Setting reference to sound recording')
        return f"A{str(uuid())}"

    def build_resource_id(self):
        """
        Builds ResourceId tag
        """
        logger.info("Building ResourceId tag.")
        tag: et.Element = et.Element(SoundRecordingTags.resource_id.value)
        add_subelement_with_text(tag, SoundRecordingTags.isrc.value, self.id)
        return tag

    def build_display_title(self):
        """
        Builds DisplayTitle tag
        """
        logger.info("Building DisplayTitle tag.")
        tag: et.Element = et.Element(SoundRecordingTags.display_title.value)
        add_subelement_with_text(tag, SoundRecordingTags.title_text.value, self.song_name)
        return tag

    def build_pline(self):
        """
        Builds PLine tag
        """
        logger.info("Building PLine tag.")
        tag: et.Element = et.Element(SoundRecordingTags.pline.value)
        add_subelement_with_text(tag, SoundRecordingTags.pline_text.value, self.pline_text)
        if self.pline_company:
            add_subelement_with_text(tag, SoundRecordingTags.pline_company.value, self.pline_company)
        if self.pline_year:
            add_subelement_with_text(tag, SoundRecordingTags.pline_year.value, self.pline_year)
        return tag

    def write(self):
        """
        Builds SoundRecording tag
        """
        logger.info("Building SoundRecording tag.")
        tag: et.Element = et.Element(ResourceListTags.sound_recording.value)
        add_subelement_with_text(tag, SoundRecordingTags.type.value, self.type)
        logger.debug('Writing type tag of sound recording')
        tag.append(self.build_resource_id())
        add_subelement_with_text(tag,
                                 SoundRecordingTags.display_title_text.value,
                                 f"{self.artist_name} - {self.song_name}"
                                 )
        tag.append(self.build_display_title())
        for party in self.party:
            tag.append(party.write())
        for contributor in self.contributor:
            tag.append(contributor.write())
        tag.append(self.build_pline())
        add_subelement_with_text(tag,
                                 SoundRecordingTags.duration.value,
                                 self.technical_details.duration,
                                 )
        add_subelement_with_text(tag,
                                 SoundRecordingTags.parental_warning_type.value,
                                 self.parental_warning_type
                                 )
        tag.append(self.technical_details.write())
        return tag


class ImageRl:
    def __init__(self,
                 resource_reference: str,
                 id_value: str,
                 type_: ImageType,
                 sender_id,
                 technical_details: et.Element):
        self.resource_reference = resource_reference
        self.id_value = id_value
        if type_ in ImageType:
            self.type = type_
        else:
            raise InvalidTypeError(type_, ImageType)
        self.sender_id = sender_id
        self.technical_details = technical_details

    def build_resource_id(self):
        tag = et.Element(ImageTags.resource_id.value)
        add_subelement_with_text(tag,
                                 ImageTags.proprietary_id.value,
                                 f"T{self.id_value}IMG",
                                 Namespace=self.sender_id)
        return tag

    def write(self):
        logger.info("Building Image tag.")
        tag = et.Element(ImageTags.root.value)
        logger.debug("Got root value.")
        add_subelement_with_text(tag,
                                 ImageTags.resource_reference.value,
                                 self.resource_reference)
        add_subelement_with_text(tag,
                                 ImageTags.type_.value,
                                 self.type)
        tag.append(self.build_resource_id())
        return tag
