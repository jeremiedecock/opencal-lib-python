import datetime
import os
import warnings
import xml.sax
from xml.sax.handler import ContentHandler, ErrorHandler

PY_DATE_FORMAT = "%Y-%m-%d"


def save_pkb(card_list, pkb_path):

    pkb_path = os.path.expanduser(pkb_path)  # to handle "~/..." paths
    pkb_path = os.path.abspath(pkb_path)     # to handle relative paths

    with open(pkb_path, 'w') as fd:
        print('<?xml version="1.0" encoding="UTF-8" standalone="no"?>', file=fd)
        print('<pkb>', file=fd)
        for card in card_list:
            cdate_str = card['cdate'].strftime(PY_DATE_FORMAT)
            hidden_str = 'true' if card['hidden'] else 'false'

            print('<card cdate="{}" hidden="{}">'.format(cdate_str, hidden_str), file=fd)

            print('<question><![CDATA[{}]]></question>'.format(card['question']), file=fd)   # TODO: escape CDATA
            print('<answer><![CDATA[{}]]></answer>'.format(card['answer']), file=fd)         # TODO: escape CDATA

            for tag in card['tags']:
                print('<tag>{}</tag>'.format(tag), file=fd)
            
            for review in card['reviews']:
                rdate_str = review['rdate'].strftime(PY_DATE_FORMAT)
                print('<review rdate="{}" result="{}"/>'.format(rdate_str, review['result']), file=fd)

            print('</card>', file=fd)
        print('</pkb>', file=fd)


def load_pkb(pkb_path):

    pkb_path = os.path.expanduser(pkb_path)  # to handle "~/..." paths
    pkb_path = os.path.abspath(pkb_path)     # to handle relative paths

    # Make XML parser
    xml_reader = xml.sax.make_parser()
    pkb_handler = PKBHandler()
    xml_reader.setContentHandler(pkb_handler)
    xml_reader.setErrorHandler(pkb_handler)

    # Parse XML files
    inputsource = xml.sax.InputSource(pkb_path)
    xml_reader.parse(inputsource)

    return pkb_handler.card_list


class PKBHandler(ContentHandler, ErrorHandler):
    """A content handler"""

    def __init__(self):
        self._card_list = []

        self._current_card = None
        self._current_question = None
        self._current_answer = None
        self._current_review = None
        self._current_tag = None

    @property
    def card_list(self):
        return self._card_list

    # ContentHandler ############################

    #def startDocument(self):
    #    print("Start document")

    #def endDocument(self):
    #    print("End document")

    def startElement(self, name, attr):
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
                        raise Exception('Unexpected value for the "hidden" attribute: got {} (expected "true" or "false")'.format(value))
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
            self._current_review = {}

            for key, value in list(attr.items()):
                if key == "rdate":
                    self._current_review[key] = datetime.datetime.strptime(value, PY_DATE_FORMAT) #.date()
                elif key == "result":
                    self._current_review[key] = value
                else:
                    raise ValueError(key)
        elif name == "tag":
            assert self._current_tag is None and self._current_card is not None
            self._current_tag = ""

    def endElement(self, name):
        #print("End element:", name)

        if name == "card":
            assert self._current_card is not None
            self._card_list.append(self._current_card)
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


    # def startElementNS(self, name, qname, attr):
    #     """TODO: improve this"""
    #     print("Start NS element:", name, qname, end=' ')
    #     for key, value in list(attr.items()):
    #         print("[", key, "=", value, "]", end=' ')
    #     print()

    # def endElementNS(self, name, qname):
    #     """TODO: improve this"""
    #     print("End NS element:", name, qname)

    def characters(self, ch):
        #print("Characters:", ch)

        if self._current_question is not None:
            self._current_question += ch

        elif self._current_answer is not None:
            self._current_answer += ch

        elif self._current_tag is not None:
            self._current_tag += ch

    # ErrorHandler ##############################

    def fatalError(self, exception):
        print("Fatal error:", exception)  # TODO

    def error(self, exception):
        print("Error:", exception)        # TODO

    def warning(self, exception):
        warnings.warn(exception)