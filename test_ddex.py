import os
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
from lxml import etree as et

#  local imports
from .utils import add_subelement_with_text, get_logger
from .config import LOG_DIR, TEST_XML_DIR, FIXTURES_DIR
from pydex.test.utils import get_data_from_xml, get_messageheader_fixture

logger = get_logger(__name__, 'tests')


# utility functions for testing


class TestUtils:
    def test_add_subelement_with_text(self):
        """Test add_subelement_with_text function."""
        logger.info('Testing add_subelement_with_text')
        tag = et.Element('root')
        add_subelement_with_text(tag, 'subelement', 'text')
        assert tag.find('subelement').text == 'text'


class TestMessageHeaders:
    def test_message_header(self):
        logger.info('Testing MessageHeader')
        #  Get data from fixture
        fixture = os.path.join(FIXTURES_DIR, 'message_header.xml')
        compare_data = get_data_from_xml(fixture)
        logger.debug(f'Getting compare data \n\t{compare_data = }')

        message_header_tag = get_messageheader_fixture()
        xmldata = get_data_from_xml(message_header_tag.write())
        logger.debug(f'Getting xmldata \n\t{xmldata = }')

        assert xmldata == compare_data


