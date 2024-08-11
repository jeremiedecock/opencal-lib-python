from typing import List, Optional, Union, Any
from datetime import datetime

from opencal.review import ConsolidationReview

PY_DATE_FORMAT = r"%Y-%m-%d"

class Card:
    def __init__(
            self,
            creation_datetime: Union[datetime, str],
            question: str,
            answer: str = "",
            is_hidden: bool = False,
            tags: Optional[List[str]] = None,
            consolidation_reviews: Optional[List[ConsolidationReview]] = None,
        ) -> None:
        """
        Initialize a Card instance.

        Parameters
        ----------
        creation_datetime : datetime
            The date and time when the card was created.
        question : str
            The question text of the card.
        answer : str, optional
            The answer text of the card (default is an empty string).
        is_hidden : bool, optional
            A flag indicating whether the card is hidden (default is False).
        tags : list of str, optional
            A list of tags associated with the card (default is None, which initializes an empty list).
        consolidation_reviews : list of ConsolidationReview, optional
            A list of consolidation reviews associated with the card (default is None, which initializes an empty list).

        Returns
        -------
        None
        """
        self.creation_datetime: datetime = creation_datetime   # TODO ?
        self.question: str = question
        self.answer: str = answer
        self.is_hidden: bool = is_hidden

        if tags is None:
            self.tags: List[str] = []
        else:
            self.tags: List[str] = tags

        if consolidation_reviews is None:
            self.consolidation_reviews: List[ConsolidationReview] = []
        else:
            self.consolidation_reviews: List[ConsolidationReview] = consolidation_reviews

        self.grade: Union[float, int] = None       # TODO?
        self.priority: Union[float, int] = None    # TODO?
        self.difficulty: Union[float, int] = None  # TODO?


    def __getitem__(self, key: str) -> Optional[Union[str, datetime, bool, List[str]]]:
        """
        Retrieve the value associated with the given key from the Card attributes.

        This method is primarily for backward compatibility with older versions of OpenCAL
        where the Card class did not exist and was replaced by a dictionary.

        Parameters
        ----------
        key : str
            The key for which the value needs to be retrieved. Valid keys are:
            "cdate", "question", "answer", "hidden", "tags", "reviews".

        Returns
        -------
        Optional[Union[str, datetime, bool, List[str]]]
            The value associated with the given key. The return type can be a string,
            datetime, boolean, or a list of strings, depending on the key.

        Raises
        ------
        KeyError
            If the key is not found in the Card attributes.
        """
        if key == "cdate":
            return self.creation_datetime
        elif key == "question":
            return self.question
        elif key == "answer":
            return self.answer
        elif key == "hidden":
            return self.is_hidden
        elif key == "tags":
            return self.tags
        elif key == "reviews":
            return self.consolidation_reviews
        elif key == "grade":
            return self.grade
        elif key == "priority":
            return self.priority
        elif key == "difficulty":
            return self.difficulty
        else:
            raise KeyError(f"Key {key} not found in Card attributes")


    def __setitem__(self, key: str, value: Any) -> None:
        """
        Set the value associated with the given key in the Card attributes.

        This method is primarily for backward compatibility with older versions of OpenCAL
        where the Card class did not exist and was replaced by a dictionary.

        Parameters
        ----------
        key : str
            The key for which the value needs to be set. Valid keys are:
            "cdate", "question", "answer", "hidden", "tags", "reviews".
        value : Any
            The value to be set for the given key. The type of value depends on the key:
            - "cdate": datetime
            - "question": str
            - "answer": str or None
            - "hidden": bool
            - "tags": list of str
            - "reviews": list of ConsolidationReview

        Returns
        -------
        None

        Raises
        ------
        TypeError
            If the value type does not match the expected type for the given key.
        KeyError
            If the key is not found in the Card attributes.
        """
        if key == "cdate":
            if isinstance(value, datetime):
                self.creation_datetime = value
            elif isinstance(value, str):
                self.creation_datetime = datetime.datetime.strptime(value, PY_DATE_FORMAT)
            else:
                raise TypeError(f"Expected datetime or string, got {type(value)}")
        elif key == "question":
            if not isinstance(value, str):
                raise TypeError(f"Expected str, got {type(value)}")
            self.question = value
        elif key == "answer":
            if (value is not None) and (not isinstance(value, str)):
                raise TypeError(f"Expected str or None, got {type(value)}")
            self.answer = value
        elif key == "hidden":
            if not isinstance(value, bool):
                raise TypeError(f"Expected bool, got {type(value)}")
            self.is_hidden = value
        elif key == "tags":
            if not isinstance(value, list):
                raise TypeError(f"Expected list, got {type(value)}")
            self.tags = value
        elif key == "reviews":
            if not isinstance(value, list):
                raise TypeError(f"Expected list, got {type(value)}")
            self.consolidation_reviews = value
        elif key == "grade":
            if not isinstance(value, (float, int)):
                raise TypeError(f"Expected float or int, got {type(value)}")
            self.grade = value
        elif key == "priority":
            if not isinstance(value, (float, int)):
                raise TypeError(f"Expected float or int, got {type(value)}")
            self.priority = value
        elif key == "difficulty":
            if not isinstance(value, (float, int)):
                raise TypeError(f"Expected float or int, got {type(value)}")
            self.difficulty = value
        else:
            raise KeyError(f"Key {key} not found in Card attributes")


    def __str__(self) -> str:
        """
        Return a string representation of the Card instance.
    
        This method provides a human-readable representation of the Card instance,
        primarily for debugging and logging purposes.
    
        Returns
        -------
        str
            A string that concatenates the question and answer attributes of the Card instance.
        """
        return f"Question: {self.question}\nAnswer: {self.answer}"
