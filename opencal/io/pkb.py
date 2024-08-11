import datetime
import opencal
from opencal.card import Card
from opencal.review import ConsolidationReview
import os
from typing import Any, Dict, List, Optional
import warnings
import xml.sax
from xml.sax.handler import ContentHandler, ErrorHandler

from opencal.core.data import RIGHT_ANSWER_STR

PY_DATE_FORMAT = r"%Y-%m-%d"

TIME_DELTA_OF_FIRST_REVIEWS = datetime.timedelta()    # Null time delta (0 day)
INIT_VALIDATED_TIME_DELTA = datetime.timedelta()      # Null time delta (0 day)


# EXCEPTION CLASSES ###########################################################

class XmlPkbError(Exception):
    """Exception raised if the XML PKB file is not valid."""
    pass


# SAVE PKB ####################################################################

def save_pkb(
        card_list: List[Card],
        pkb_path: str
    ) -> None:
    """
    Save the personal knowledge base (PKB) to an XML file.

    This function takes a list of cards and saves them to the specified
    PKB path in XML format. Each card contains information such as creation
    date, hidden status, question, answer, tags, and reviews.

    Parameters
    ----------
    card_list : List[Card]
        A list of cards.
    pkb_path : str
        The file path where the PKB should be saved. This path can include
        user home directory shortcuts (e.g., "~/...") and relative paths.

    Returns
    -------
    None
    """

    pkb_path = opencal.path.expand_path(pkb_path)

    with open(pkb_path, 'w') as fd:
        fd.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
        fd.write('<pkb>\n')
        for card in card_list:
            cdate_str = card.creation_datetime.strftime(PY_DATE_FORMAT)
            hidden_str = 'true' if card.is_hidden else 'false'

            fd.write(f'<card cdate="{cdate_str}" hidden="{hidden_str}">\n')

            # In the following code, the "]]>" is replaced by "]]]]><![CDATA[>"
            # to avoid premature end of the CDATA section by XML parser ("CDATA nesting").
            # See the following links for more details:
            # - https://en.wikipedia.org/wiki/CDATA#Nesting
            # - https://en.wikipedia.org/wiki/CDATA#Issues_with_encoding
            # - https://stackoverflow.com/questions/223652/is-there-a-way-to-escape-a-cdata-end-token-in-xml

            question_str = card.question.replace("]]>", "]]]]><![CDATA[>")
            fd.write(f'<question><![CDATA[{question_str}]]></question>\n')
            if card.answer == '':
                fd.write('<answer/>\n')
            else:
                answer_str = card.answer.replace("]]>", "]]]]><![CDATA[>")
                fd.write(f'<answer><![CDATA[{answer_str}]]></answer>\n')

            for tag in card.tags:
                fd.write(f'<tag>{tag}</tag>\n')
            
            for review in card.consolidation_reviews:
                if isinstance(review, ConsolidationReview):
                    rdate_str = review.review_datetime.strftime(PY_DATE_FORMAT)
                    result_str = "good" if review.is_right_answer else "bad"
                    fd.write(f'<review rdate="{rdate_str}" result="{result_str}"/>\n')
                elif isinstance(review, dict): # TODO: Temporary workaround for backward compatibility
                    rdate_str = review['rdate'].strftime(PY_DATE_FORMAT)
                    fd.write(f'<review rdate="{rdate_str}" result="{review["result"]}"/>\n')
                else:
                    raise ValueError(f"Unexpected review type: {type(review)}")

            fd.write('</card>\n')
        fd.write('</pkb>\n')


# LOAD PKB ####################################################################

def load_pkb(pkb_path: str) -> List[Card]:
    """
    Load the personal knowledge base (PKB) from an XML file.

    This function reads the PKB from the specified XML file path and parses
    it into a list of cards.

    Parameters
    ----------
    pkb_path : str
        The file path from which the PKB should be loaded. This path can include
        user home directory shortcuts (e.g., "~/...") and relative paths.

    Returns
    -------
    List[Card]
        A list of cards.
    """

    pkb_path = opencal.path.expand_path(pkb_path)

    # Make XML parser
    xml_reader = xml.sax.make_parser()
    pkb_handler = PKBHandler()
    xml_reader.setContentHandler(pkb_handler)
    xml_reader.setErrorHandler(pkb_handler)

    # Parse XML files
    inputsource = xml.sax.InputSource("file://" + pkb_path)
    xml_reader.parse(inputsource)

    return pkb_handler.card_list


class PKBHandler(ContentHandler, ErrorHandler):
    """A content handler"""

    def __init__(self) -> None:
        """
        Initialize the PKBHandler.

        This constructor initializes the PKBHandler with empty structures
        to store the parsed data from the XML file. It sets up lists and
        dictionaries to hold card information, questions, answers, reviews,
        and tags.

        Parameters
        ----------
        None

        Returns
        -------
        None
        """
        self._card_list: List[Card] = []

        self._current_card: Optional[Card] = None
        self._current_question: Optional[str] = None
        self._current_answer: Optional[str] = None
        self._current_review: Optional[ConsolidationReview] = None
        self._current_tag: Optional[str] = None

    @property
    def card_list(self) -> List[Card]:
        """
        Get the list of cards.

        This property returns the list of cards parsed from the XML file.

        Returns
        -------
        List[Card]
            A list of cards.
        """
        return self._card_list

    # ContentHandler ############################

    #def startDocument(self):
    #    print("Start document")

    #def endDocument(self):
    #    print("End document")

    def startElement(
            self,
            name: str,
            attr: Dict[str, str]
        ) -> None:
        """
        Handle the start of an XML element.

        This method is called by the XML parser when it encounters the start
        of an element. It processes the element and its attributes, updating
        the current state of the handler.

        Parameters
        ----------
        name : str
            The name of the XML element.
        attr : Dict[str, str]
            The attributes of the XML element.

        Returns
        -------
        None
        """
        #print("Start element:", name, end=' ')
        #for key, value in list(attr.items()):
        #    print("[", key, "=", value, "]", end=' ')
        #print()
         
        if name == "card":
            assert self._current_card is None
            self._current_card = {"reviews": [], "tags": []}

            for key, value in list(attr.items()):
                if key == "cdate":
                    self._current_card[key] = datetime.datetime.strptime(value, PY_DATE_FORMAT) #.date()
                elif key == "hidden":
                    if value == "true":
                        self._current_card[key] = True
                    elif value == "false":
                        self._current_card[key] = False
                    else:
                        raise Exception(f'Unexpected value for the "hidden" attribute: got {value} (expected "true" or "false")')
                else:
                    raise ValueError(key)
        elif name == "question":
            assert self._current_question is None and self._current_card is not None
            self._current_question = ""
        elif name == "answer":
            assert self._current_answer is None and self._current_card is not None
            self._current_answer = ""
        elif name == "review":
            assert self._current_review is None and self._current_card is not None

            review_date = None
            is_right_answer = None

            for key, value in list(attr.items()):
                if key == "rdate":
                    review_date = datetime.datetime.strptime(value, PY_DATE_FORMAT) #.date()
                elif key == "result":
                    if value == 'good':
                        is_right_answer = True
                    elif value == 'bad':
                        is_right_answer = False
                    else:
                        raise ValueError(f'Unknown result value "{value}"')
                else:
                    raise ValueError(f"Unknown XML attribute {key}")

            if (review_date is not None) and (is_right_answer is not None):
                self._current_review =  ConsolidationReview(
                    review_datetime=review_date,
                    is_right_answer=is_right_answer
                )
            else:
                raise ValueError('"rdate" and "result" must be defined')
        elif name == "tag":
            assert self._current_tag is None and self._current_card is not None
            self._current_tag = ""

    def endElement(
            self,
            name: str
        ) -> None:
        """
        Handle the end of an XML element.

        This method is called by the XML parser when it encounters the end
        of an element. It processes the element and updates the current state
        of the handler.

        Parameters
        ----------
        name : str
            The name of the XML element.

        Returns
        -------
        None
        """
        #print("End element:", name)

        if name == "card":
            assert self._current_card is not None

            current_card = Card(
                creation_datetime=self._current_card["cdate"],
                question=self._current_card["question"],
                answer=self._current_card["answer"],
                is_hidden=self._current_card["hidden"],
                tags=self._current_card["tags"],
                consolidation_reviews=self._current_card["reviews"]
            )

            # Sort reviews ("in-place")
            current_card.consolidation_reviews.sort(key=lambda review: review.review_datetime)

            # TODO: IS THE FOLLOWING CODE REALLY USEFUL???
            # Add the "timedelta" and "last_validated_timedelta" attributes to each "review"
            if len(current_card.consolidation_reviews) > 0:
                current_card.consolidation_reviews[0].timedelta = TIME_DELTA_OF_FIRST_REVIEWS
                current_card.consolidation_reviews[0].last_validated_timedelta = INIT_VALIDATED_TIME_DELTA

                for i in range(1, len(current_card.consolidation_reviews)):
                    previous_timedelta = current_card.consolidation_reviews[i-1].timedelta
                    is_right_previous_answer = current_card.consolidation_reviews[i-1].is_right_answer
                    current_card.consolidation_reviews[i].last_validated_timedelta = previous_timedelta if is_right_previous_answer else INIT_VALIDATED_TIME_DELTA

                    dt1 = current_card.consolidation_reviews[i-1].review_datetime
                    dt2 = current_card.consolidation_reviews[i].review_datetime
                    current_card.consolidation_reviews[i].timedelta = dt2 - dt1

            self._card_list.append(current_card)
            self._current_card = None
        elif name == "question":
            assert self._current_question is not None and self._current_card is not None
            self._current_card["question"] = self._current_question
            self._current_question = None
        elif name == "answer":
            assert self._current_answer is not None and self._current_card is not None
            self._current_card["answer"] = self._current_answer
            self._current_answer = None
        elif name == "review":
            assert self._current_review is not None and self._current_card is not None
            self._current_card["reviews"].append(self._current_review)
            self._current_review = None
        elif name == "tag":
            assert self._current_tag is not None and self._current_card is not None
            self._current_card["tags"].append(self._current_tag)
            self._current_tag = None


    def characters(
            self,
            ch: str
        ) -> None:
        """
        Handle character data within an XML element.

        Parameters
        ----------
        ch : str
            The character data.
        
        Returns
        -------
        None
        """
        #print("Characters:", ch)

        if self._current_question is not None:
            self._current_question += ch

        elif self._current_answer is not None:
            self._current_answer += ch

        elif self._current_tag is not None:
            self._current_tag += ch

    # ErrorHandler ##############################

    def fatalError(
            self,
            exception: xml.sax.SAXParseException
        ) -> None:
        """
        Handle a fatal error during XML parsing.

        Parameters
        ----------
        exception : xml.sax.SAXParseException
            The exception that was raised.
        
        Returns
        -------
        None
        """
        print("Fatal error:", exception)  # TODO

    def error(
            self,
            exception: xml.sax.SAXParseException
        ) -> None:
        """
        Handle a non-fatal error during XML parsing.

        Parameters
        ----------
        exception : xml.sax.SAXParseException
            The exception that was raised.
        
        Returns
        -------
        None
        """
        print("Error:", exception)        # TODO

    def warning(
            self,
            exception: xml.sax.SAXParseException
        ) -> None:
        """
        Handle a warning during XML parsing.

        Parameters
        ----------
        exception : xml.sax.SAXParseException
            The exception that was raised.
        
        Returns
        -------
        None
        """
        warnings.warn(exception)


# DEBUG #######################################################################

def main() -> None:
    """
    Main function to load and save the personal knowledge base (PKB).

    This function loads the PKB from the path specified in the configuration
    then save it in another file.

    This function is used for debugging purposes (c.f. `.vscode/launch.json`).

    Parameters
    ----------
    None

    Returns
    -------
    None
    """
    load_pkb_path = opencal.cfg["opencal"]["pkb_path"]
    save_pkb_path = "/tmp/debug.pkb"   # opencal.cfg["opencal"]["pkb_path"]

    print(f"Loading PKB from {load_pkb_path}")
    card_list = load_pkb(load_pkb_path)

    # print(card_list)

    print(f"Saving PKB to {save_pkb_path}")
    save_pkb(card_list, save_pkb_path)


if __name__ == "__main__":
    main()
