"""
@Author: Nebil G.
"""

import os

# Constants
CONST_OK = "OK"
CONST_OVERWRITTEN = "UEBERSCHRIEBEN"
CONST_NO_DATA = "no data"


class BaseParser:
    def __init__(self, filename=None, url=None, source_string=None):
        """

        exact one of the following three parameters MUST be provided
        :param filename:    the filename in parseable format
        :param url:         the url in parseable format
        :param source_string: a valid string to parse

        this Method saves the values in instance variables and invokes the
        object creation in public Method set_source of descendant
        """

        self.__filename = filename
        self.__url = url
        self.__source_string = source_string

        self.__saved_values_in_dict = {}  # key + value-list pair
        #self.__list_of_selectable_keys=[]

        # analyze the source and prepare the object on base of the data in descendant
        self.set_source(filename, url, source_string)

    # ###################### start GETTER - Methods ########################
    def get_url(self) -> str:
        return self.__url

    def set_url(self, url):
        self.__url = url

    def get_filename(self) -> str:
        return self.__filename

    def set_filename(self, filename):
        self.__filename = filename

    def get_source_string(self) -> str:
        return self.__source_string

    def set_source_string(self, source_string):
        self.__source_string = source_string

    # ###################### END GETTER - Methods ########################

    def set_source(self, filename=None, url=None, source_string=None) -> str:
        """ First set the source
            this Method returns OK in case of success,
            otherwise the errorstring will be returned
        """
        if not filename and not url and not source_string:
            raise Exception("DV-Error: Es muss mindestens einer der drei Parameter uebergeben werden")

        # if filename:
        #     if not os.path(filename):
        #         raise Exception("DV-Error: Die angegebene Datei existiert nicht!")

        return CONST_OK

    def find_possible_keynames_all(self) -> dict:
        """ This Method MUST be implemented in the concrete descendant and should
            return all possible names, which can be selected for searching data and the
            corresponding first value to display at the GUI (value if needed)
            {'lon':123, 'lat' : 23, 'name' : 'hanspeter'}, empty {} for the case something went wrong
        """
        pass

    def find_possible_keypath(self, search_string) -> str:
        """ This Method MUST be implemented in the concrete descendant and should
             return for one keyname the corresponding fullpath-Name, how it is accessible
             {'lon':123, 'lat' : 23, 'name' : '{"hanspeter":12'}, empty "" for the case something went wrong
             search_string = hanspeter returns $name.hanspeter as keyname
         """
        pass

    def scan_values(self, name, keypath) -> list:
        """

        This method returns values for a specific key and saves them in a dict for later usage

        :param name:    whatevername, with this name the data will be stored and can later be retrieved
        :param keypath: the full path on how the values from the object can be fetchend
        :return:        list of the values e.g. [1,2,8,9,11...]
        """
        pass

    def get_values(self, name) -> list:
        """
        :param name: keyname, for which the the datavalues to return from existing DICT
        :return:     returns always list with 2 elements
                    # [0] = keyname full path
                    # [1] = allvalues could also be a list or a dict
        """
        if name in self.__saved_values_in_dict.keys():
            return self.__saved_values_in_dict[name]
        else:
            return list[CONST_NO_DATA]

    def set_values(self, name, values) -> str:
        """
        :param name: name in which the data to save in existing DICT
        :param values: values as list for the data which should be stored in the DICT
        :return:     returns always list with 2 elements

        """
        if name in self.__saved_values_in_dict.keys():
            self.__saved_values_in_dict[name] = values
            return CONST_OVERWRITTEN
        else:
            self.__saved_values_in_dict[name] = values
            return CONST_OK
