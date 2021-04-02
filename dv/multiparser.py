import dv.jsonparser

# import xmlparser, csvparser, sqlparser (TODO: need implmentation!)
from dv.jsonparser import jsonParser


class multiParser():
    def __init__(self, filename=None, url=None, sourcestring=None):
        #if not filename and not url and not sourcestring:
            #raise return "Es muss mindestens einer der drei Parameter uebergeben werden"

        # url -> getstring
        # string -> nothing
        # file -> filename
        # ... instantiate depending on extension
        # if csv -> csvobj .. jsonobj...
        self._parseObject = jsonParser(filename, url, sourcestring)
        print("ParseObjekt=", self._parseObject)

    def get_parseobject(self):
        return self._parseObject

    """ First set the source 
        this Method returns empty sting in case of success,
        otherwise the errorstring will be returned
    """
    def set_source(self, filename=None, url=None, sourcestring=None):
        return self.__init__(filename, url, sourcestring);

    """ internal """

    def find_possible_keynames_all(self):
        return self.get_parseobject().find_possible_keynames_all()

    def find_possible_keypath(self, searchstring):
        return self.get_parseobject().find_possible_keypath(searchstring)

    def scan_values(self, name, keypath):
        # scan for all values of given keypath
        return self.get_parseobject().scan_values(name, keypath)

    def get_values(self, name):
        return self.get_parseobject().dictSavedValues[name]
