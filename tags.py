"""
Author: iamu985
DateCreated: 2023-02-08 08:09PM
Github: https://iamu985.github.io

Includes all the xml tags that are required to write into xml document.
"""

from enum import Enum, EnumMeta


#  Overriding the default EnumMeta __contains__ implementation
#  to return True if the item exists and False if it does not

class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True

#  Type Sets
class MessageControlType(Enum, metaclass=MetaEnum):
    test = "TestMessage"
    live = "LiveMessage"


class MessagePartyType(Enum, metaclass=MetaEnum):
    sender = "Sender"
    receiver = "Receiver"


class SoundRecordingType(Enum, metaclass=MetaEnum):
    audio_stem = "AudioStem"
    clip = "Clip"
    musical_work_readalong_sound_recording = "MusicalWorkReadalongSoundRecording"
    musical_work_sound_recording = "MusicalWorkSoundRecording"
    non_musical_work_readalong_sound_recording = "NonMusicalWorkReadalongSoundRecording"
    non_musical_work_sound_recording = "NonMusicalWorkSoundRecording"
    spoken_word_sound_recording = "SpokenWordSoundRecording"
    unknown = "Unknown"
    user_defined = "UserDefined"


class TechnicalDetailsType(Enum, metaclass=MetaEnum):
    audio = "Audio"
    image = "Image"


class PartyType(Enum):
    artist = "Artist"
    contributor = "Contributor"


class ParentalWarningType(Enum, metaclass=MetaEnum):
    explicit = "Explicit"
    unknown = "Unknown"
    non_explicit = "NonExplicit"
    user_defined = "UserDefined"


class ImageType(Enum, metaclass=MetaEnum):
    front_cover_image = "FrontCoverImage"
    preview_image = "PreviewImage"


#  Tag Sets
class MessageHeaderTags(Enum):
    root = "MessageHeader"
    thread_id = "MessageThreadId"
    message_id = "MessageId"
    message_created_date_time = "MessageCreatedDateTime"
    message_control_type = "MessageControlType"


class MessagePartyTags(Enum):
    sender = "MessageSender"
    receiver = "MessageRecipient"
    party_id = "PartyId"
    party_name = "PartyName"
    full_name = "FullName"


class PartyListTags(Enum):
    root = "PartyList"
    party = "Party"
    party_reference = "PartyReference"
    party_name = "PartyName"
    full_name = "FullName"


class ResourceListTags(Enum):
    root = "ResourceList"
    sound_recording = "SoundRecording"
    image = "Image"


class SoundRecordingTags(Enum):
    resource_reference = "ResourceReference"
    type = "Type"
    resource_id = "ResourceId"
    isrc = "ISRC"
    display_title_text = "DisplayTitleText"
    display_title = "DisplayTitle"
    title_text = "TitleText"
    pline = "PLine"
    pline_text = "PLineText"
    pline_company = "PLineCompany"
    pline_year = "PLineYear"
    duration = "Duration"
    parental_warning_type = "ParentalWarningType"


class TechnicalDetailsTags(Enum):
    root = "TechnicalDetails"
    details_reference = "TechnicalResourceDetailsReference"
    audio_codec = "AudioCodecType"
    channels = "NumberOfChannels"
    sample_rate = "SamplingRate"
    bitrate = "BitsPerSample"
    duration = "Duration"
    file = "File"
    uri = "URI"
    hash_sum = "HashSum"
    algorithm = "Algorithm"
    hash_sum_value = "HashSumValue"
    image_height = "ImageHeight"
    image_width = "ImageWidth"


class ImageTags(Enum):
    root = "Image"
    resource_reference = "ResourceReference"
    type_ = "Type"
    resource_id = "ResourceId"
    proprietary_id = "ProprietaryId"

