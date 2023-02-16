"""
Author: iamu985
DateCreated: 2023-02-10 02:26PM
Github: https://iamu985.github.io

Builds MessageHeader section of the xml document.
"""
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from lxml import etree as et
from uuid import uuid4 as uuid
from datetime import datetime

# local imports
from pydex.utils import get_logger, add_subelement_with_text
from pydex.tags import (MessageHeaderTags,
                        MessageControlType,
                        MessagePartyTags,
                        MessagePartyType)
from pydex.exceptions import InvalidPartyType

logger = get_logger(__name__, 'ddex')


class MessageHeader:
    """
    Builds MessageHeader tag
    """

    def __init__(self,
                 sender: et.Element,
                 receiver: et.Element,
                 message_control_type: MessageControlType = MessageControlType.live.value,
                 ):
        self.sender = sender
        self.receiver = receiver
        self.message_control_type = message_control_type
        if self.message_control_type == MessageControlType.test.value:
            self.thread_id = 'Test0'
            self.message_id = 'Test1'
        else:
            self.thread_id = str(uuid())
            self.message_id = str(uuid())
        self.created_datetime = datetime.now()

    def get_formatted_datetime(self) -> str:
        if self.message_control_type == MessageControlType.test.value:
            logger.debug('Is in test mode')
            logger.debug('Formatting datetime object.')
            return self.created_datetime.strftime("%Y-%m-%d")
        logger.debug('Formatting datetime object.')
        return self.created_datetime.strftime("%Y-%m-%dT%H:%M:%S")

    def write(self) -> et.Element:
        logger.info("Writing MessageHeader section to xml document.")
        tag: et.Element = et.Element(MessageHeaderTags.root.value)
        add_subelement_with_text(tag, MessageHeaderTags.thread_id.value, self.thread_id)
        add_subelement_with_text(tag, MessageHeaderTags.message_id.value, self.message_id)

        tag.append(self.sender.write())
        tag.append(self.receiver.write())
        add_subelement_with_text(tag, MessageHeaderTags.message_created_date_time.value, self.get_formatted_datetime())
        add_subelement_with_text(tag, MessageHeaderTags.message_control_type.value, self.message_control_type)
        return tag


class MessageParty:
    """
    Sender or Receiver Object
    """

    def __init__(self,
                 party_id: str,
                 full_name: str,
                 role: MessagePartyType = MessagePartyType.sender.value,
                 ):
        self.party_id = party_id
        self.full_name = full_name
        self.role = role
    
    def assign_role(self):
        """
        Assigns appropriate tag according to the role provided.
        If Sender is provided then it assigns MessageSender and vice versa
        """
        if self.role == MessagePartyType.sender.value:
            return MessagePartyTags.sender.value
        if self.role == MessagePartyType.receiver.value:
            return MessagePartyTags.receiver.value
        else:
            raise InvalidPartyType(self.role)

    def build_party_name(self) -> et.Element:
        tag: et.Element = et.Element(MessagePartyTags.party_name.value)
        add_subelement_with_text(tag, MessagePartyTags.full_name.value, self.full_name)
        return tag

    def write(self) -> et.Element:
        tag = et.Element(self.assign_role())
        add_subelement_with_text(tag, MessagePartyTags.party_id.value, self.party_id)
        tag.append(self.build_party_name())
        return tag


if __name__ == "__main__":
    from test.utils import get_messageheader_fixture
    from utils import save
    from config import TEST_XML_DIR

    root = get_messageheader_fixture()
    output_file = "messageheader_test.xml"
    save(root.write(), output_file)
