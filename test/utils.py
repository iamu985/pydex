import sys

sys.path.append('..')
from lxml import etree as et
import xmltodict
from pydex.messageheader import MessageHeader, MessageParty
from pydex.tags import MessageHeaderTags, MessagePartyTags, MessageControlType
from pydex.utils import get_logger

logger = get_logger(__name__, 'tests')


def get_data_from_xml(xml_obj):
    """
    Return a dictionary of data from an xml object.
    xml_obj: lxml.etree._Element or filepath
    """
    if isinstance(xml_obj, str):
        logger.info('Is instance str')
        with open(xml_obj, 'r') as f:
            logger.info(f'Reading file {xml_obj}')
            tree = et.parse(f)  # Get tree from xml file
            return xmltodict.parse(et.tostring(tree))
    if isinstance(xml_obj, et._Element):
        logger.info('Is instance lxml.etree._Element')
        logger.info(f'Generating tree from {type(xml_obj)}')
        tree = et.ElementTree(xml_obj)
        return xmltodict.parse(et.tostring(tree))
    else:
        logger.error(f'xml_obj is not a valid type: {type(xml_obj)}')
        raise TypeError(f'xml_obj is not a valid type: {type(xml_obj)} must be str or lxml.etree._Element')


def get_sender():
    """Return a MessageParty object for the sender."""
    return MessageParty(party_id='PADPIDA2015010310U', full_name='Sender')


def get_receiver():
    """Return a MessageParty object for the receiver."""
    return MessageParty(party_id='PADPIDA2016091404E', full_name='Receiver')


def get_messageheader_fixture():
    """Return a list of MessageHeader objects."""
    sender = get_sender()
    receiver = get_receiver()
    return MessageHeader(
        sender=sender,
        receiver=receiver,
        message_control_type=MessageControlType.test.value
    )
