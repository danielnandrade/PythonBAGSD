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
import dv.baseparser as dvm
import json
from jsonpath_ng import jsonpath, parse

from dv.baseparser import baseParser

class jsonParser(baseParser):
    def __init__(self, filename=None, url=None, sourcestring=None):
        super().__init__(filename, url, sourcestring)
        self.set_source(filename, url, sourcestring)

    def set_source(self, filename=None, url=None, sourcestring=None):
        s = ""
        if not filename and not url and not sourcestring:
            return "Es muss mindestens einer der drei Parameter uebergeben werden"

        try:
            if sourcestring:
                self.jsonobj = json.loads(sourcestring)
                self.filename = filename
                self.sourcestring = sourcestring
            elif filename:
                with open(filename) as f:
                    self.jsonobj = json.load(f)
                self.filename = filename
            elif url:  # jsonstring aus url holen
                import requests
                self.sourcestring = requests.get(url).json()
                self.url = url
                self.jsonobj.loads(self.sourcestring)
            else:
                s = "Parameters are incorrect"
        except Exception as e:
            s = e.errno
            print(s)

        return s

    """ internal """

    """ This Method searches in the jsonobject each valid key which can contain data
        with the first possible value (for presentation purposes) and returns it as dict
        {'lon':123, 'lat' : 23, 'name' : 'hanspeter'}, empty {} for the case something went wrong
    """
    def find_possible_keynames_all(self):
        rdict = {}

        for k,v in self.jsonobj.items():
            if isinstance(v, dict):
                rdict[k] = "{dictLevel1}"
                self._find_possible_keynames_dict(v, rdict)
            elif isinstance(v, list):
                rdict[k+"[*]"] = "[list]"
                self._find_possible_keynames_dict(v[0], rdict)
            else:
                rdict[str(k)] = str(v)

            #print("rdict=",rdict)
        return rdict

    def _find_possible_keynames_dict(self, d, sumd):
        if not isinstance(d, dict):
            if isinstance(d, list):
                self._find_possible_keynames_list(d, sumd)
                # wenn keine dict dann hier raus
            return

        #print("dict=",d, type(d))
        for k, v in d.items():
            if isinstance(v, dict):
                sumd[k] = "{dict}"
                self._find_possible_keynames_dict(v, sumd)
            elif isinstance(v, list):
                sumd[k+"[0]"] = "[list]"
                if isinstance(v[0],dict):
                    self._find_possible_keynames_list(v[0], sumd)
                elif isinstance(v[0], list):
                    self._find_possible_keynames_list(v[0], sumd)
                else:
                    sumd[k] = str(v)
            else:
                sumd[k] = str(v)

    def _find_possible_keynames_list(self, l, sumd):
        if not isinstance(l, list):
            if isinstance(l, dict):
                self._find_possible_keynames_dict(l, sumd)
                # wenn keine List dann hier raus
            return

        for row in l:
            if isinstance(row, dict):
                sumd[row] = "{dict in Liste}"
                #self.find_possible_keynames_dict(v,sumd)
            elif isinstance(row, list):
                sumd[row+"[0]"] = "[list in Liste]"
                #self.find_possible_keynames_list(v, sumd)
            else:
                #sumd[row] = str(v)
                sumd[str(row)] = "[irgendwas in Liste]"



    def find_possible_keypath(self, searchstring):
        if not self.jsonobj:
            raise Exception("Es konnte kein JSON-Objekt erkannt werden, wurde die init-Methode aufgerufen ?")

        # check if index argument ist provided and remove it temporary, because its not part of the json
        s = searchstring.split('[')
        searchstring_idx=""
        if len(s) > 1:
            searchstring=s[0]
            searchstring_idx = "["+s[1]


        self.possible_path=[]
        if searchstring in self.jsonobj.keys():  # found in root
            self.possible_path.append(searchstring)

        else: # nicht im Haupt-Dict-Key, also weitersuchen recursiv in inneren Objekten
            for dict_key, dict_value in self.jsonobj.items():
                # check type and depending on this continue search
                print("Level1: ",dict_key)
                if isinstance(dict_value,dict):
                    if self._find_possible_key_path_in_dict(searchstring, dict_value): # if found
                        self.possible_path.append(dict_key)
                        break
                elif isinstance(dict_value,list):
                    if isinstance(dict_value[0],dict):
                        if self._find_possible_key_path_in_dict(searchstring, dict_value[0]):
                            self.possible_path.append(dict_key + "[*]")
                            break
                    elif isinstance(dict_value[0],list):
                        if self._find_possible_key_path_in_list0(searchstring, dict_value[0]):
                            self.possible_path.append(dict_key + "[*]")
                            break

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
    def _find_possible_key_path_in_list0(self, searchstring, search_list):
        for list_value in search_list:
            print("LevelY: ",list_value)
            if isinstance(list_value,dict):
                if self._find_possible_key_path_in_dict(searchstring, list_value): # found
                    return True

            elif isinstance(list_value,list):
                if self._find_possible_key_path_in_list0(searchstring, list_value[0]): # found
                    return True
            else:
                continue

    def _find_possible_key_path_in_dict(self, searchstring, search_dict):
        if isinstance(search_dict, dict):
            # if in keys, found
            if searchstring in search_dict.keys():  # found
                self.possible_path.append(searchstring)
                return True

            for dict_key, dict_value in search_dict.items():
                print("LevelX: ",dict_key)
                if isinstance(dict_value,dict):
                    if self._find_possible_key_path_in_dict(searchstring, dict_value): # found
                        self.possible_path.append(dict_key)
                        return True

                elif isinstance(dict_value,list):
                    if len(dict_value) > 0:
                        if isinstance(dict_value[0],dict):
                            if self._find_possible_key_path_in_dict(searchstring, dict_value[0]): # found
                                self.possible_path.append(dict_key+"[*]")
                                return True
                            elif self._find_possible_key_path_in_list0(searchstring, dict_value[0]): # found
                                self.possible_path.append("[*]")
                                return True

                elif dict_key == searchstring:
                    # gefunden, nicht weiter suchen noetig
                    self.possible_path.append(searchstring)
                    return True

    def scan_values(self, name, keypath):
        # jsonstring is already filled during init constructor otherwise all cant work
        # path to search e.g. to features/alert in {"features":{"alert":"myval"}}
        # store values in {name: [keypath, [values]]}

        # look for the path
        jsonpath_expression = parse(keypath)#'$.features[*].geometry.coordinates[0]')  # parse('$.id')

        # match = jsonpath_expression.find(json_data)[0]
        x = [match.value for match in jsonpath_expression.find(self.jsonobj)]

        listkeypath_and_values = [keypath, x]
        self.dictSavedValues[name] = listkeypath_and_values
        return x

    def get_values(self, name):
        if name in self.dictSavedValues.keys():
            return self.dictSavedValues[name]
        else:
            return "['no data']"
