import logging
import os
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from datetime import datetime
from lxml import etree as et
from hashlib import md5

#  local imports
from pydex.config import LOG_DIR, TEST_XML_DIR


def get_logger(name, logfile):
    """Return a logger object."""
    path_to_log = os.path.join(LOG_DIR, logfile)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    # create a file handler
    handler = logging.FileHandler(f'{path_to_log}.log', mode='w')
    handler.setLevel(logging.DEBUG)
    # create a logging format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s\n')
    handler.setFormatter(formatter)
    # add the handlers to the logger
    logger.addHandler(handler)
    return logger


logger = get_logger(__name__, 'tests')


def add_subelement_with_text(parent, tag, text, **attrib):
    """Add a subelement with text to parent element."""
    logger.debug(f'Adding subelement {tag} with text {text} to parent {parent.tag}\n')
    element = et.SubElement(parent, tag, **attrib)
    element.text = text


def save(root_element, output_filename):
    """
    Saves xml file.
    """
    path_to_save = os.path.join(TEST_XML_DIR, output_filename)
    logger.debug(f'Saving xml file to {path_to_save}\n')
    tree = et.ElementTree(root_element)
    logger.debug(f'Generating tree {tree}\n')
    logger.debug(f'Writing tree to file {path_to_save}\n')
    tree.write(path_to_save, pretty_print=True)


def get_initials(full_name):
    """Get initials from full name."""
    initials = ""
    for word in full_name.split(' '):
        initials += word[0]
    return initials


def format_duration(duration: int) -> str:
    """Format duration to match ddex standard ie PT00H00M00S"""
    s = int(duration % 60)
    m = int(duration // 60)
    if m >=60:
        h = int(m // 60)
        m = int(m % 60)
        if h < 10:
            h = f"0{h}"
        if m < 10:
            m = f"0{m}"
        return f"PT{h}H{m}M{s}S"
    else:
        if m < 10:
            m = f"0{m}"
        return f"PT{m}M{s}S"


def compute_image_hash(image_file):
    """
    Computes image hash
    """
    logger.debug('Computing hash for image.')
    with open(image_file, 'rb') as image_bytes:
        hash_value = md5()
        while chunk := image_bytes.read(9000):
            hash_value.update(chunk)
        return hash_value.hexdigest()
