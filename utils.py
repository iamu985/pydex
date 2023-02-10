import logging
import os
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))
from .config import LOG_DIR, TEST_XML_DIR
from datetime import datetime
from lxml import etree as et


def get_logger(name, logfile):
    """Return a logger object."""
    path_to_log = os.path.join(LOG_DIR, logfile)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler(f'{path_to_log}.log', mode='w')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


logger = get_logger(__name__, 'tests')


def add_subelement_with_text(parent, tag, text, **attrib):
    """Add a subelement with text to parent element."""
    element = et.SubElement(parent, tag, **attrib)
    element.text = text


def save(root_element, output_filename):
    """
    Saves xml file.
    """
    path_to_save = os.path.join(TEST_XML_DIR, output_filename)
    logger.debug(f'Saving xml file to {path_to_save}')
    tree = et.ElementTree(root_element)
    logger.debug(f'Generating tree {tree}')
    logger.debug(f'Writing tree to file {path_to_save}')
    tree.write(path_to_save, pretty_print=True)


def get_initials(full_name):
    """Get initials from full name."""
    initials = ""
    for word in full_name.split(' '):
        initials += word[0]
    return initials
