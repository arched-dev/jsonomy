import datetime
import re
from typing import Any, Dict, List
from dateutil.parser import parse


def is_date(string: str) -> tuple[bool, datetime] | tuple[bool, str]:
    """
    Checks if a string can be parsed into a date.

    Args:
        string (str): The string to be checked.

    Returns:
        bool: True if the string can be parsed into a date, False otherwise.
        str: The parsed date if the string is a date, otherwise the original string.
    """
    if isinstance(string, str) and len(string) > 6 and any(x in string for x in ["-", ":", "/"]):
        try:
            return True, parse(string)
        except ValueError:
            pass

    return False, string


def convert_camel_to_snake(name: str) -> str:
    """
    Converts a camel case string to snake case.

    Args:
        name (str): The string to be converted.

    Returns:
        str: The converted string.
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class Jsonomy:
    """
    Designed to format data from a JSON response.
    It includes methods to convert camel case to snake case,
    identify and parse strings that represent dates,
    and recursively process data structures.
    """

    def __init__(self, data: Any):
        """Initializes the JSONFormatter with the data to be processed."""
        self.data = data

    def process_dict(self, val: Dict) -> Dict:
        """
        Processes a dictionary, converting keys to snake case and recursively processing the values.

        Args:
            val (Dict): The dictionary to be processed.

        Returns:
            Dict: The processed dictionary.
        """
        if isinstance(val, dict):
            return {convert_camel_to_snake(k): self.process_value(v) for k, v in val.items()}
        return val

    def process_list(self, val: List) -> List:
        """
        Processes a list, recursively processing its elements.

        Args:
            val (List): The list to be processed.

        Returns:
            List: The processed list.
        """
        if isinstance(val, list):
            return [self.process_value(v) for v in val]
        return val

    def process_value(self, val: Any) -> Any:
        """
        Processes a value. If the value is a string, it is checked to see if it is a date.
        If the value is a dictionary or a list, it is processed recursively.

        Args:
            val (Any): The value to be processed.

        Returns:
            Any: The processed value.
        """
        if isinstance(val, str):
            date_found, parsed = is_date(val)
            if date_found:
                return parsed
        if isinstance(val, dict):
            return self.process_dict(val)
        if isinstance(val, list):
            return self.process_list(val)
        return val

    def format(self) -> Any:
        """
        Starts the processing of the data.

        Returns:
            Any: The processed data.
        """
        return self.process_value(self.data)

    def pprint(self) -> None:
        """
        Pretty prints the processed data.
        """
        import pprint
        pprint.pprint(self.format())
