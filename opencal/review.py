from typing import List, Optional, Union, Any
from datetime import datetime

PY_DATE_FORMAT = r"%Y-%m-%d"

class ConsolidationReview:
    def __init__(
            self,
            review_datetime: Union[datetime, str],
            is_right_answer: bool,
            user_response_time_ms: Optional[int] = None
        ) -> None:
        """
        Initialize a Review instance.

        Parameters
        ----------
        review_datetime : Union[datetime, str]
            The date and time when the review was conducted. Can be a datetime object or a string.
        is_right_answer : bool
            A flag indicating whether the user's answer was correct.
        user_response_time_ms : Optional[int], optional
            The time taken by the user to respond, in milliseconds (default is None).

        Returns
        -------
        None
        """
        self.review_datetime: datetime = review_datetime    # TODO ?
        self.is_right_answer: bool = is_right_answer        # TODO ?
        self.user_response_time_ms: Optional[int] = user_response_time_ms


    def __getitem__(self, key: str) -> Union[str, datetime]:
        """
        Retrieve the value associated with the given key from the Review attributes.

        This method is primarily for backward compatibility with older versions of OpenCAL
        where the Review class did not exist and was replaced by a dictionary.

        Parameters
        ----------
        key : str
            The key for which the value needs to be retrieved. Valid keys are:
            "rdate", "result".

        Returns
        -------
        Union[str, datetime]
            The value associated with the given key. The return type can be a string or datetime,
            depending on the key.

        Raises
        ------
        KeyError
            If the key is not found in the Review attributes.
        """
        if key == "rdate":
            return self.review_datetime  # TODO
        elif key == "result":
            return "good" if self.is_right_answer else "bad"
        else:
            raise KeyError(f"Key {key} not found in Review attributes")

    
    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value associated with the given key in the Review attributes.
    
        This method is primarily for backward compatibility with older versions of OpenCAL
        where the Review class did not exist and was replaced by a dictionary.
    
        Parameters
        ----------
        key : str
            The key for which the value needs to be set. Valid keys are:
            "rdate", "result".
        value : Any
            The value to be set for the given key. The type of value depends on the key:
            - "rdate": datetime or str
            - "result": bool or str
    
        Returns
        -------
        None
    
        Raises
        ------
        TypeError
            If the value type does not match the expected type for the given key.
        KeyError
            If the key is not found in the Review attributes.
        """
        if key == "rdate":
            if isinstance(value, datetime):
                self.review_datetime: datetime = value
            elif isinstance(value, str):
                self.review_datetime: datetime = datetime.strptime(value, PY_DATE_FORMAT)
            else:
                raise TypeError(f"Expected datetime or string, got {type(value)}")
        elif key == "result":
            if isinstance(value, bool):
                self.is_right_answer: bool = value
            elif isinstance(value, str):
                self.is_right_answer: bool = value == "good"
            else:
                raise TypeError(f"Expected boolean or string, got {type(value)}")
        else:
            raise KeyError(f"Key {key} not found in Review attributes")


    def __str__(self) -> str:
        """
        Return a string representation of the Review instance.

        This method provides a human-readable representation of the Review instance,
        primarily for debugging and logging purposes.

        Returns
        -------
        str
            A string that concatenates the review_datetime and is_right_answer attributes of the Review instance.
        """
        return f"{self.review_datetime}, {self.is_right_answer}"
