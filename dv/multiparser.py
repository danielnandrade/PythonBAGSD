import dv.jsonparser

# import xmlparser, csvparser, sqlparser (TODO: need implmentation!)
from dv.jsonparser import JsonParser
from dv.csvparser import CsvParser
import os.path


class MultiParser:
    def __init__(self, filename=None, url=None, source_string=None, delimiter=",", headerrow=True, col_date=(), col_float=None):
        # url -> getstring
        # string -> nothing
        # file -> filename
        # ... instantiate depending on extension
        # if csv -> csvobj .. jsonobj...
        if os.path.isfile(filename):
            filesplit = os.path.splitext(filename)
            if len(filesplit) > 0:
                if filesplit[1] == ".json":
                    self.__parseObject = JsonParser(filename, url, source_string)
                elif filesplit[1] == ".csv":
                    self.__parseObject = CsvParser(filename, url, source_string, delimiter, headerrow, col_date, col_float)
                else:
                    raise Exception("Datei aktuell nicht unterstützt")

        print("ParseObjekt=", self.get_parseobject())

    def get_parseobject(self):
        return self.__parseObject

    def set_source(self, filename=None, url=None, source_string=None, delimiter=",", headerrow=True, col_date=(), col_float=None):
        return self.__init__(filename, url, source_string, delimiter, headerrow, col_date, col_float)

    def find_possible_keynames_all(self):
        return self.get_parseobject().find_possible_keynames_all()

    def find_possible_keypath(self, search_string) -> str:
        return self.get_parseobject().find_possible_keypath(search_string)

    def scan_values(self, name, keypath):
        # scan for all values of given keypath
        return self.get_parseobject().scan_values(name, keypath)

    def get_values(self, name):
        return self.get_parseobject().get_values(name)
