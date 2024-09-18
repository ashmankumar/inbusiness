import os
import yaml
from src.Constants import DEFAULT_CONSTANTS


def load_key_from_config(key: str) -> str:
    """
    Load the specified key from the config.yml file, environment variables, or a global constants dictionary.

    Args:
        key (str): The key to search for.

    Returns:
        str: The value associated with the key.

    Raises:
        ValueError: If the key is not found in any of the sources.
    """
    # Attempt to load from config.yml
    try:
        with open('config.yml', 'r') as file:
            config = yaml.safe_load(file)
            value = config.get(key)
    except FileNotFoundError:
        value = None
        print("config.yml not found")

    # Check environment variables if the key is not found in the config file
    if not value:
        value = os.getenv(key.upper())

    # Check the global constants if the key is still not found
    if not value:
        value = DEFAULT_CONSTANTS.get(key)

    # Throw an error if the key is not found in any of the sources
    if not value:
        raise ValueError(f"{key} not found in config file, environment variables, or constants")

    return value
