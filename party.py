import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from lxml import etree as et
from uuid import uuid4 as uuid
from datetime import datetime

#  local imports
from .utils import get_logger, add_subelement_with_text, get_initials
from .tags import PartyListTags, PartyTypeTags

logger = get_logger(__name__, 'ddex')


class Party:
    """
    Builds Party tag
    A party can be an artist of a contributor.
    """

    def __init__(self,
                 party_type: str,
                 full_name: str,
                 ):
        self.party_type = party_type  # Artist or Contributor
        self.full_name = full_name
        self.id = self.uuid()

    def get_reference(self):
        logger.debug(f'Getting reference to party of type {self.party_type}')
        initials = get_initials(self.full_name)
        return f'P{initials}{str(self.id)}'  # Returns a unique id for the party
    # in format PHRK1024-1024-1024-1024

    def write(self):
        logger.info("Building Party tag.")
        tag: et.Element = et.Element(PartyListTags.party.value)
        add_subelement_with_text(tag, PartyListTags.party_reference.value, self.get_reference())

        #  Building PartyName
        logger.info("Building PartyName tag.")
        party_name_tag: et.Element = et.Element(PartyListTags.party_name.value)
        add_subelement_with_text(party_name_tag, PartyListTags.full_name.value, self.full_name)
        tag.append(party_name_tag)

        return tag

