import os
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
from lxml import etree as et

#  local imports
import pytest
import re
from uuid import uuid4 as uuid
from pydex.utils import add_subelement_with_text, get_logger, format_duration
from pydex.config import LOG_DIR, TEST_XML_DIR, FIXTURES_DIR
from pydex.tags import (MessagePartyTags,
                        MessageControlType,
                        MessageHeaderTags,
                        MessagePartyType,
                        ResourceListTags,
                        TechnicalDetailsTags,
                        TechnicalDetailsType,
                        SoundRecordingType,
                        ParentalWarningType,
                        PartyType,
                        ImageTags,
                        ImageType,
                        )
from pydex.messageheader import MessageHeader, MessageParty
from pydex.resource_builder import (ResourceList,
                                    TechnicalDetails,
                                    SoundRecording,
                                    ImageRl
                                    )
from pydex.party import Party


logger = get_logger(__name__, 'tests')


#  fixtures
@pytest.fixture(name='sender')
def fixture_sender():
    return MessageParty(
        party_id='123456789',
        full_name='Test Sender',
        role=MessagePartyType.sender.value,
    )


@pytest.fixture(name='receiver')
def fixture_receiver():
    return MessageParty(
        party_id='987654321',
        full_name='Test Receiver',
        role=MessagePartyType.receiver.value,
    )


@pytest.fixture(name='messageheader')
def fixture_messageheader(sender, receiver):
    return MessageHeader(
        sender=sender,
        receiver=receiver,
        message_control_type=MessageControlType.live.value
    )


@pytest.fixture(name='parties')
def fixture_parties():
    return [
            Party(
                party_type=PartyType.artist.value,
                full_name=f"Test Artist {i}"
                )
            for i in range(3)
            ]


@pytest.fixture(name='contributors')
def fixture_contributors():
    return [
            Party(
                party_type=PartyType.contributor.value,
                full_name=f"Test Contributor {i}"
                )
            for i in range(3)
            ]


@pytest.fixture(name='technicaldetails_audio')
def fixture_technicaldetails_audio():
    return TechnicalDetails(
            type_=TechnicalDetailsType.audio.value,
            file="./resources/audio.mp3",
            resource_uuid=str(uuid()),
            )

@pytest.fixture(name='technicaldetails_image')
def fixture_technicaldetails_image():
    return TechnicalDetails(
            type_=TechnicalDetailsType.image.value,
            file="./resources/image.jpg",
            resource_uuid=str(uuid()),
            )

@pytest.fixture(name='soundrecording')
def fixture_soundrecording(technicaldetails_audio, parties, contributors):
    return SoundRecording(
            type_=SoundRecordingType.musical_work_sound_recording.value,
            id_="123456789",
            song_name="Test Song",
            artist_name='Test Artist',
            pline_text="2023 Record Label",
            parental_warning_type=ParentalWarningType.non_explicit.value,
            technical_details=technicaldetails_audio,
            party=parties,
            contributor=contributors,
            )


@pytest.fixture(name='image')
def fixture_image(technicaldetails_image):
    return ImageRl(
            resource_reference="INF8081",
            id_value="123456789",
            type_=ImageType.front_cover_image.value,
            sender_id="PAPI9012849",
            technical_details=technicaldetails_image,
            )


@pytest.fixture(name='resourcelist')
def fixture_resourcelist(soundrecording, image):
    return ResourceList(
            sound_recording=[soundrecording],
            image=image
            )


class TestUtils:
    """Test suite for utils module functions"""
    def test_add_subelement_with_text(self):
        """Test add_subelement_with_text function."""
        logger.debug('Testing add_subelement_with_text\n')
        tag = et.Element('root')
        add_subelement_with_text(tag, 'subelement', 'text')
        assert tag.find('subelement').text == 'text'

    def test_format_duration(self):
        """Test if the function produces correct strings"""
        logger.debug("Testing format_duration function.")
        duration = 220
        expression = r"PT([0-9]{2}H)?[0-9]{2}M[0-9]{2}S"
        assert re.match(expression, format_duration(duration))

    def test_format_duration_hour(self):
        """
        Test if the function produces correct string for hour as well.
        """
        logger.debug("Testing format_duration function for hour as well.")
        duration = 3740
        expression = r"PT([0-9]{2}H)?[0-9]{2}M[0-9]{2}S"
        assert re.match(expression, format_duration(duration))


class TestMessageParty:
    """Test suite for every part of MessageParty section of DDEX xml file"""
    def test_message_party_sender_tag(self):
        """Test if sender tag is correct."""
        logger.debug('Testing if sender tag is correct.\n')
        assert MessagePartyTags.sender.value == 'MessageSender'

    def test_message_party_receiver_tag(self):
        """Test if receiver tag is correct."""
        logger.debug('Testing if receiver tag is correct.\n')
        assert MessagePartyTags.receiver.value == 'MessageRecipient'

    def test_message_party_sender_object_tag(self, sender):
        """Test if root generated by the builder has the correct MessageSender tag."""
        logger.debug('Testing if root generated by the builder has the correct MessageSender tag.\n')
        root = sender.write()
        assert root.tag == MessagePartyTags.sender.value

    def test_message_party_receiver_object_tag(self, receiver):
        """Test if root generated by the builder has the correct MessageRecipient tag."""
        logger.debug('Testing if root generated by the builder has the correct MessageRecipient tag.\n')
        root = receiver.write()
        assert root.tag == MessagePartyTags.receiver.value

    def test_message_party_has_party_name(self, sender):
        """Test if MessageSender tag has PartyName tag."""
        logger.debug('Testing if MessageSender tag has PartyName tag.\n')
        root = sender.write()
        assert root.find(MessagePartyTags.party_name.value) is not None

    def test_message_party_name_has_full_name(self, sender):
        """Test MessageParty class."""
        logger.debug('Testing if message party name has full name.\n')
        root = sender.write()
        for children in root.getchildren():
            if children.tag == MessagePartyTags.party_name.value:
                assert children.find(MessagePartyTags.full_name.value) is not None


class TestMessageHeader:
    def test_message_header_root_tag(self):
        """
        Test message header root tag is MessageHeader
        """
        assert MessageHeaderTags.root.value == "MessageHeader"

    def test_message_header_thread_id_tag(self):
        logger.debug('Testing MessageThreadId tag is correct.')
        assert MessageHeaderTags.thread_id.value == "MessageThreadId"

    def test_message_header_message_id_tag(self):
        logger.debug('Testing MessageId tag is correct.')
        assert MessageHeaderTags.message_id.value == "MessageId"

    def test_message_header_datetime_tag(self):
        logger.debug('Testing MessageCreatedDateTime tag is correct.')
        assert MessageHeaderTags.message_created_date_time.value == "MessageCreatedDateTime"

    def test_message_header_control_type_tag(self):
        logger.debug('Testing MessageControlType tag is correct.')
        assert MessageHeaderTags.message_control_type.value == "MessageControlType"

    def test_message_header_tag_ordering(self, messageheader):
        logger.debug('Testing the order of tags is correct.')
        correct_ordering = [
                MessageHeaderTags.thread_id.value,
                MessageHeaderTags.message_id.value,
                MessagePartyTags.sender.value,
                MessagePartyTags.receiver.value,
                MessageHeaderTags.message_created_date_time.value,
                MessageHeaderTags.message_control_type.value,
                ]
        root = messageheader.write()
        root_ordering = [children.tag for children in root.getchildren()]
        assert correct_ordering == root_ordering


class TestResourceList:
    def test_resource_list_root_tag(self):
        logger.debug('Testing ResourceList tag is correct.')
        assert ResourceListTags.root.value == "ResourceList"

    def test_resource_list_sound_recording_tag(self):
        logger.debug('Testing SoundRecording tag is correct.')
        assert ResourceListTags.sound_recording.value == "SoundRecording"

    def test_resource_list_image_tag(self):
        logger.debug('Testing Image tag is correct.')
        assert ResourceListTags.image.value == "Image"

    def test_resource_list_ordering(self, resourcelist):
        logger.debug('Testing the order of ResourceList tags are correct.')
        correct_order = []
        #  check if resourcelist.soundrecording is a list type
        if isinstance(resourcelist.sound_recording, list):
            logger.debug('Type of SoundRecording received is list')
        else:
            logger.error(f'Type of SoundRecording is not a list. Got {type(resourcelist.sound_recording)}')
        for i in resourcelist.sound_recording:
            correct_order.append(ResourceListTags.sound_recording.value)
        correct_order.append(ResourceListTags.image.value)
        root = resourcelist.write()
        root_order = [children.tag for children in root.getchildren()]
        assert correct_order == root_order


class TestTechnicalDetails:
    def test_technical_details_root(self):
        assert TechnicalDetailsTags.root.value == "TechnicalDetails"

    def test_technical_details_reference_tag(self):
        assert TechnicalDetailsTags.details_reference.value == "TechnicalResourceDetailsReference"

    def test_technical_details_audio_codec_type_tag(self):
        assert TechnicalDetailsTags.audio_codec.value == "AudioCodecType"

    def test_technical_details_number_of_channels_tag(self):
        assert TechnicalDetailsTags.channels.value == "NumberOfChannels"

    def test_technical_details_sampling_rate_tag(self):
        assert TechnicalDetailsTags.sample_rate.value == "SamplingRate"

    def test_technical_details_bits_per_sample_tag(self):
        assert TechnicalDetailsTags.bitrate.value == "BitsPerSample"

    def test_technical_details_duration_tag(self):
        assert TechnicalDetailsTags.duration.value == "Duration"

    def test_technical_details_file_tag(self):
        assert TechnicalDetailsTags.file.value == "File"

    def test_technical_details_uri_tag(self):
        assert TechnicalDetailsTags.uri.value == "URI"

    def test_technical_details_hash_sum_tag(self):
        assert TechnicalDetailsTags.hash_sum.value == "HashSum"

    def test_technical_details_hash_sum_algorithm_tag(self):
        assert TechnicalDetailsTags.algorithm.value == "Algorithm"

    def test_technical_details_hash_sum_value_tag(self):
        assert TechnicalDetailsTags.hash_sum_value.value == "HashSumValue"

    def test_technical_details_image_height_tag(self):
        assert TechnicalDetailsTags.image_height.value == "ImageHeight"

    def test_technical_details_image_height_tag(self):
        assert TechnicalDetailsTags.image_width.value == "ImageWidth"

    def test_technical_details_image_type_value(self):
        assert TechnicalDetailsType.image.value == "Image"

    def test_technical_details_audio_type_value(self):
        assert TechnicalDetailsType.audio.value == "Audio"

    def test_technical_details_write_method(self, technicaldetails_audio):
        logger.info(f'Testing write method of {technicaldetails_audio}')
        logger.debug(f"AudioTag: {technicaldetails_audio.build_audio_technical_details().tag}")
        root = technicaldetails_audio.write()
        assert root.tag == TechnicalDetailsTags.root.value

    def test_technical_details_build_audio_method(self, technicaldetails_audio):
        logger.info(f"Testing build_audio_method for TechnicalDetails.")
        root = technicaldetails_audio.build_audio_technical_details()
        logger.debug(f"Got root from technicaldetails_audio: {root}")
        assert root.tag == TechnicalDetailsTags.root.value

    def test_technical_details_duration_format(self, technicaldetails_audio):
        #  Tests if duration is in correct ddex format
        # i.e. PT00H00M00S or PT00M00S
        expression = r"PT([0-9]{2}H)?[0-9]{2}M[0-9]{2}S"
        logger.debug(f"Technical details audio received from fixtures {technicaldetails_audio}")
        assert re.match(expression, technicaldetails_audio.duration)

    def test_technical_details_audio_type_ordering(self, technicaldetails_audio):
        correct_order = [
                TechnicalDetailsTags.details_reference.value,
                TechnicalDetailsTags.audio_codec.value,
                TechnicalDetailsTags.channels.value,
                TechnicalDetailsTags.sample_rate.value,
                TechnicalDetailsTags.bitrate.value,
                TechnicalDetailsTags.duration.value,
                TechnicalDetailsTags.file.value,
                ]
        logger.debug(f"Received TechnicalDetails audio from fixtures {technicaldetails_audio}")
        root = technicaldetails_audio.write()
        root_order = [children.tag for children in root.getchildren()]
        assert correct_order == root_order

    def test_technical_details_image_type_ordering(self, technicaldetails_image):
        correct_order = [
                TechnicalDetailsTags.details_reference.value,
                TechnicalDetailsTags.image_height.value,
                TechnicalDetailsTags.image_width.value,
                TechnicalDetailsTags.file.value,
                ]
        root = technicaldetails_image.write()
        root_order = [children.tag for children in root.getchildren()]
        assert correct_order == root_order


class TestImage:
    def test_image_root_tag(self):
        logger.info("Testing root of Image is correct.")
        assert ImageTags.root.value == "Image"

    def test_image_resource_reference_tag(self):
        logger.info("Testing resource_reference tag of Image is correct.")
        assert ImageTags.resource_reference.value == "ResourceReference"

    def test_image_type_tag(self):
        logger.info("Testing type tag of Image is correct.")
        assert ImageTags.type_.value == "Type"

    def test_image_resource_id_tag(self):
        logger.info("Testing resource_id tag of Image is correct.")
        assert ImageTags.resource_id.value == "ResourceId"

    def test_image_proprietary_id_tag(self):
        logger.info("Testing proprietary_id of Image is correct.")
        assert ImageTags.proprietary_id.value == "ProprietaryId"

    def test_image_write_method(self, image):
        logger.info("Testing write method of Image gives the correct tag.")
        root = image.write()
        assert root.tag == ImageTags.root.value


if __name__ == "__main__":
    print(file)
