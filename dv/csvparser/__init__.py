"""

This Object is a wrapper for all activities around the CSV - Files

"""
import csv
from dv.baseparser import BaseParser, CONST_EMPTY
from datetime import datetime

class CsvParser(BaseParser):
    def __init__(self, filename=None, url=None, source_string=None, delimiter=",", headerrow=True, col_date=(), col_float=None):

        super().__init__(filename, url, source_string)
        # analyze the source and prepare the object on base of the data in descendant
        self.set_source(filename, url, source_string, delimiter, headerrow, col_date, col_float)

    def set_source(self, filename=None, url=None, source_string=None, delimiter=",", headerrow=True, col_date=(), col_float=None) -> str:
        """
            # additional Parameters:
            # delimiter
            # headerrow: T/F if header is available or not. TRUE = dict mit Namen verfügbar, FALSE: Namen sind Col1,Col2..
            # col_Date: if the cols provided should be strp to Date, then argument is tuple (colnameToConvert, format in the csv e.g. %Y%m%d)
            # col_float: if the col should be converted to float
        """
        try:
            s = super().set_source(filename, url, source_string)

            if source_string:
                self.__prepare_object_reader(list(csv.reader(source_string, delimiter=delimiter)), headerrow, col_date, col_float)
            elif filename:
                with open(filename) as f:
                    self.__prepare_object_reader(list(csv.reader(f, delimiter=delimiter)), headerrow, col_date, col_float)
            elif url:
                import requests
                self.set_source_string(requests.get(url))
                self.__prepare_object_reader(list(csv.reader(self.get_source_string(), delimiter)), headerrow, col_date, col_float)
            else:
                s = "Parameters are incorrect"
        except Exception as e:
            s = e.args
            print(s)

        return s

    # prepare the CSV into a Dict-Object for faster & structured access
    def __prepare_object_reader(self, csv_list, headerrow, col_date, col_float):
        objdict = {}

        # initial preparation of headers
        colHeadernames = []
        col = csv_list[0]
        if headerrow:
            colHeadernames = col
        else:
            # no header specified, create ids
            for idx in range(0, len(col)):
                colHeadernames.append(str(idx))

        # initial preparation of dict-Arrays per csv-col
        for idx in range(0, len(colHeadernames)):
            objdict[colHeadernames[idx]] = []

        for col in csv_list[1:]:
            spalte = 0
            for colval in col:
                # umwandeln in date oder float falls gewuenscht
                #if col_float and col_float == colHeadernames[spalte]:
                if str(colval).isdigit():
                    colval = float(colval)

                if col_date and col_date[0] == colHeadernames[spalte]:
                    colval = datetime.strptime(colval, "%Y%m%d")

                objdict[colHeadernames[spalte]].append(colval)
                spalte += 1

        self.set_object_reader(objdict)
        self.set_values_all(objdict)

    def find_possible_keynames_all(self) -> dict:
        rdict = {}

        if self.get_object_reader():
            if isinstance(self.get_object_reader(), dict):
                for k, v in self.get_object_reader().items():
                    rdict[k] = ""

        print("ALL=", rdict)
        return rdict

    def find_possible_keypath(self, search_string) -> str:
        """

        :param      search_string: the name with or without the whole path, but the name must be present
        :return:    the complete path to retrieve related values, in CSV it is always the same.
                    If key doesnt exist retruns empty

        """
        if not self.get_object_reader():
            raise Exception("Es konnte kein CSV-Objekt erkannt werden, wurde die init-Methode aufgerufen ?")

        if isinstance(self.get_object_reader(), dict):
            if search_string in self.get_object_reader().keys():
                return search_string # key exists can be used

        return CONST_EMPTY

    def scan_values(self, name, keypath) -> list:
        """

        This method returns values for a specific key and saves them in a dict for later usage

        :param name:    in CSV its not relevant, as its flat in Row/Col
        :param keypath: the full path (in CSV=Colname or Colnumber) on how the values from the object can be fetched,
                        if syntax is not VALID exception is raised
        :return:        list of the values e.g. [1,2,8,9,11...]
        """
        # list of all possible values is already filled during init constructor otherwise all cant work
        # path to search e.g. to "0"/Zeitstempel in Col1, Col3, Zeitstempel,Col99 \n 0,"3","20160102"
        # store values in {name: [keypath, [values]]}

        return self.get_object_reader()[keypath]
