"""
Author: iamu985
DateCreated: 2023-02-08 08:09PM
Github: https://iamu985.github.io

Includes all the xml tags that are required to write into xml document.
"""

from enum import Enum


class MessageHeaderTags(Enum):
    root = "MessageHeader"
    thread_id = "MessageThreadId"
    message_id = "MessageId"
    message_created_date_time = "MessageCreatedDateTime"
    message_control_type = "MessageControlType"


class MessageControlType(Enum):
    test = "TestMessage"
    live = "LiveMessage"


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


class PartyTypeTags(Enum):
    artist = "Artist"
    contributor = "Contributor"


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
