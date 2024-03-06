import hashlib
import json
from typing import Dict, Any
from pip._internal.operations import freeze

def dict_hash(dictionary: Dict[str, Any]) -> str:
    """MD5 hash of a dictionary."""
    dhash = hashlib.md5()
    # We need to sort arguments so {'a': 1, 'b': 2} is
    # the same as {'b': 2, 'a': 1}
    encoded = json.dumps(dictionary, sort_keys=True).encode()
    dhash.update(encoded)
    return dhash.hexdigest()

def package_list() -> list:
    pkgs = freeze.freeze()
    req=[pkg for pkg in pkgs]
    return req