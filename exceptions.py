"""
Collection of all custom error classes.
"""
import sys
from pathlib import Path

file = Path(__file__).resolve()
package_root_directory = file.parents[1]
sys.path.append(str(package_root_directory))

from pydex.tags import MessagePartyTags

class InvalidTypeError(Exception):
    """
    Error class for invalid type.
    """

    def __init__(self, type_, type_obj):
        self.type = type_
        self.message = f"Invalid type: {self.type}. Expected\n"
        for types in type_obj:
            self.message += types
        super().__init__(self.message)


class InvalidPartyType(Exception):
    """
    Error class for Invalid Party type.
    """
    def __init__(self, type_):
        self.type = type_
        self.message = f"Invalid MessageParty type. Expected" \
                f"{MessagePartyTags.sender.value}" \
                f"or {MessagePartyTags.receiver.value}." \
                f"Got {self.type}"


class MissingAttribute(Exception):
    """
    Raises MissingAttribute error if theres any attribute missing that is 
    required to build a DDEX object.
    """
    def __init__(self, codec_type):
        self.codec_type = codec_type
        self.message = f"Missing a required attribute sender_id for codec type {self.codec_type}"
