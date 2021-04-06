"""
Precondition: pip install jsonpath_ng
Dokumentation here: https://pypi.org/project/jsonpath-ng/

$	the root object/element
@	the current object/element
. or []	child operator
..	recursive descent. JSONPath borrows this syntax from E4X.
*	wildcard. All objects/elements regardless their names.
[]	subscript operator. XPath uses it to iterate over element collections and for predicates. In Javascript and JSON it is the native array operator.
[,]	Union operator in XPath results in a combination of node sets. JSONPath allows alternate names or array indices as a set.
[start:end:step]	array slice operator borrowed from ES4.
?()	applies a filter (script) expression.
()	script expression, using the underlying script engine.

In addition:
The following Methods expects that Lists are always with same types, only first item will be analyzed
"""
import json
from jsonpath_ng import jsonpath, parse
from dv.baseparser import BaseParser


class JsonParser(BaseParser):
    def __init__(self, filename=None, url=None, source_string=None) -> str:

        # init -> triggers automatically set_source in baseObject
        return super().__init__(filename, url, source_string)

    def set_source(self, filename=None, url=None, source_string=None) -> str:
        try:
            s = super().set_source(filename, url, source_string)
            print ("Hello")
            if source_string:
                self.jsonobj = json.loads(source_string)
            elif filename:
                with open(filename) as f:
                    self.jsonobj = json.load(f)
            elif url:  # jsonstring aus url holen
                import requests
                self.set_source_string(json.dumps(requests.get(url).json()))
                self.jsonobj = json.loads(self.get_source_string())
            else:
                s = "Parameters are incorrect"
        except Exception as e:
            s = e.args
            print(s)

        return s

    def find_possible_keynames_all(self) -> dict:
        rdict = {}
        print(self.jsonobj)
        if isinstance(self.jsonobj, dict):
            for k, v in self.jsonobj.items():
                if isinstance(v, dict):
                    rdict[k] = "{dictLevel1}"
                    self.__find_possible_keynames_dict(v, rdict)
                elif isinstance(v, list):
                    rdict[k+"[*]"] = "[list]"
                    self.__find_possible_keynames_dict(v[0], rdict)
                else:
                    rdict[str(k)] = str(v)
        elif isinstance(self.jsonobj, list):
            self.__find_possible_keynames_list(self.jsonobj[0], rdict)
        #print("ALL=", rdict)
        return rdict

    def __find_possible_keynames_dict(self, d, sumd):
        if not isinstance(d, dict):
            if isinstance(d, list):
                self.__find_possible_keynames_list(d, sumd)
                # wenn keine dict dann hier raus
            return

        for k, v in d.items():
            if isinstance(v, dict):
                sumd[k] = "{dict}"
                self.__find_possible_keynames_dict(v, sumd)
            elif isinstance(v, list):
                sumd[k+"[0]"] = "[list]"
                if isinstance(v[0], dict):
                    self.__find_possible_keynames_list(v[0], sumd)
                elif isinstance(v[0], list):
                    self.__find_possible_keynames_list(v[0], sumd)
                else:
                    sumd[k] = str(v)
            else:
                sumd[k] = str(v)

    def __find_possible_keynames_list(self, list_to_check, sumd):
        if not isinstance(list_to_check, list):
            if isinstance(list_to_check, dict):
                self.__find_possible_keynames_dict(list_to_check, sumd)
                # wenn keine List dann hier raus
            return

        for row in list_to_check:
            if isinstance(row, dict):
                sumd[row] = "[*]"
                #self.find_possible_keynames_dict(row,sumd)
            elif isinstance(row, list):
                sumd[row+"[0]"] = "[list in Liste]"
                #self.find_possible_keynames_list(v, sumd)
            else:
                #sumd[row] = str(v)
                sumd[str(row)] = "[irgendwas in Liste]"

    def find_possible_keypath(self, search_string) -> str:
        """

        :param search_string: the name with or without the whole path, but the name must be present
        :return: the complete path to retrieve related values

        """
        if not self.jsonobj:
            raise Exception("Es konnte kein JSON-Objekt erkannt werden, wurde die init-Methode aufgerufen ?")

        # only if not starting with root ($), when root is provided trust the path and dont look for fullpath
        if "$" in search_string:
            return search_string

        # check if index argument ist provided and remove it temporary, because its not part of the json
        searchstring_idx = ""
        tmps = search_string.split('[')
        if len(tmps) > 1:
            search_string=tmps[0]
            searchstring_idx = "["+tmps[1]

        self.possible_path=[]

        # hauptzweig ist dict oder list
        if isinstance(self.jsonobj, dict):
            if search_string in self.jsonobj.keys():  # found in root
                self.possible_path.append(search_string)
            else: # nicht im Haupt-Dict-Key, also weitersuchen recursiv in inneren Objekten
                for dict_key, dict_value in self.jsonobj.items():
                    # check type and depending on this continue search
                    print("Level1: ", dict_key)
                    if isinstance(dict_value, dict):
                        if self.__find_possible_key_path_in_dict(search_string, dict_value): # if found
                            self.possible_path.append(dict_key)
                            break
                    elif isinstance(dict_value, list):
                        if isinstance(dict_value[0], dict):
                            if self.__find_possible_key_path_in_dict(search_string, dict_value[0]):
                                self.possible_path.append(dict_key + "[*]")
                                break
                        elif isinstance(dict_value[0], list):
                            if self.__find_possible_key_path_in_list0(search_string, dict_value[0]):
                                self.possible_path.append(dict_key + "[*]")
                                break
        else: # kein dict, sondern list im hauptzweig
            if isinstance(self.jsonobj, list):
                if isinstance(self.jsonobj[0], dict):
                    if self.__find_possible_key_path_in_dict(search_string, self.jsonobj[0]):
                        self.possible_path.append("[*]")
                elif isinstance(self.jsonobj[0], list):
                    if self.__find_possible_key_path_in_list0(search_string, self.jsonobj[0]):
                        self.possible_path.append("[*]")

        rs = ".".join(self.possible_path[::-1])

        if len(rs) > 0:
            rs = "$."+rs
            # check we removed temp the idx now set it back
            if len(searchstring_idx) > 0:
                rs += searchstring_idx
        else:
            rs = ""

        print(rs)
        return rs

    # returns tuple(T/F found or not, value when found)
    def __find_possible_key_path_in_list0(self, search_string, search_list) -> bool:
        """
        PRIVATE method specific for json
        :param search_string:  search_string
        :param search_list:   list object in which to search
        :return:              true when found, false when not found
        """
        for list_value in search_list:
            print("LevelY: ", list_value)
            if isinstance(list_value,dict):
                if self.__find_possible_key_path_in_dict(search_string, list_value): # found
                    return True

            elif isinstance(list_value, list):
                if self.__find_possible_key_path_in_list0(search_string, list_value[0]): # found
                    return True
            else:
                continue
        return False

    def __find_possible_key_path_in_dict(self, search_string, search_dict)-> bool:
        """
        PRIVATE method specific for json
        :param search_string:  search_string
        :param search_dict:   dict in which to search
        :return:              true when found, false when not found
        """
        if isinstance(search_dict, dict):
            # if in keys, found
            if search_string in search_dict.keys():  # found
                self.possible_path.append(search_string)
                return True

            for dict_key, dict_value in search_dict.items():
                print("LevelX: ", dict_key)
                if isinstance(dict_value, dict):
                    if self.__find_possible_key_path_in_dict(search_string, dict_value): # found
                        self.possible_path.append(dict_key)
                        return True

                elif isinstance(dict_value, list):
                    if len(dict_value) > 0:
                        if isinstance(dict_value[0], dict):
                            if self.__find_possible_key_path_in_dict(search_string, dict_value[0]): # found
                                self.possible_path.append(dict_key+"[*]")
                                return True
                            elif self.__find_possible_key_path_in_list0(search_string, dict_value[0]): # found
                                self.possible_path.append("[*]")
                                return True

                elif dict_key == search_string:
                    # gefunden, nicht weiter suchen noetig
                    self.possible_path.append(search_string)
                    return True

            # if not found in any of the hirarchie
            return False

    def scan_values(self, name, keypath) -> list:
        """

        This method returns values for a specific key and saves them in a dict for later usage

        :param name:    whatevername, with this name the data will be stored and can later be retrieved
        :param keypath: the full path on how the values from the object can be fetched,
                        if syntax is not VALID exception is raised
        :return:        list of the values e.g. [1,2,8,9,11...]
        """
        # jsonstring is already filled during init constructor otherwise all cant work
        # path to search e.g. to features/alert in {"features":{"alert":"myval"}}
        # store values in {name: [keypath, [values]]}

        # look for the path
        jsonpath_expression = parse(keypath)#'$.features[*].geometry.coordinates[0]')  # parse('$.id')

        # match = jsonpath_expression.find(json_data)[0]
        x = [match.value for match in jsonpath_expression.find(self.jsonobj)]
        if len(x) == 1:
            x = x[0]

        listkeypath_and_values = [keypath, x]
        #self.__dict_saved_values[name] = listkeypath_and_values
        super().set_values(name, listkeypath_and_values)
        return x
