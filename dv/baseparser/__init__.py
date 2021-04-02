"""
@Author: Nebil G.
This is the only Object to instantiate, this will handle all FileTypes as a wrapper and forward the
implementation to the corresponding object
"""
class baseParser():
    def __init__(self, filename=None, url=None, sourcestring=None):
        self.filename = filename
        self.url = url
        self.jsonstring = sourcestring
        self.dictSavedValues = {}
        #self.set_source(filename, url, sourcestring);
        self.list_of_possible_keypaths=[]

    """ First set the source 
        this Method returns empty sting in case of success,
        otherwise the errorstring will be returned
    """
    def set_source(self, filename=None, url=None, sourcestring=None):
        s = ""
        if not filename and not url and not sourcestring:
            return "Es muss mindestens einer der drei Parameter uebergeben werden"

        return s

    """ internal """

    """ This Method should search for all posibble keynames and return them
        {'lon':123, 'lat' : 23, 'name' : 'hanspeter'}, empty {} for the case something went wrong
    """
    def find_possible_keynames_all(self):
        self.masterparser.find_possible_keynames_all()

    def find_possible_keypath(self, searchstring):
        pass

    def scan_values(self, name, keypath):
        # scan for all values of given keypath
        pass

    def get_values(self, name):
        return self.dictSavedValues[name]
