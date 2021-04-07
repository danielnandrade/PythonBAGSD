
import multiparser as js

##########################################################################
############     EXAMPLE ILLUSTRATION OF MULTIPARSER           ###########
##########################################################################

# Sources
# JSON Samples
#fname="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/PythonBAGSD/country.json"
#fname="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/eq_data_1_day_m1.json"
#fname="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/testdaten/eq_putt.json"
#fname="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/owid-covid-data_deu.json"
#fname="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/kap_13_Pegel_Bonn.json"

#obj = js.multiParser(source_string="{"testuser":"Nebil","kurs":"Python"}")
#obj = js.multiParser(filename=fname)
#obj = js.multiParser(url="https://covid.ourworldindata.org/data/owid-covid-data.json")

fname = "C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/testdaten/testdump.csv"
# XML Samples
obj = js.MultiParser(filename=fname, headerrow=False, col_date=("Zeitstempel","%Y%m%d"), col_float="Wert")

vals = obj.find_possible_keynames_all()
if len(vals) > 0:
     vals = list(vals.keys())
#     print("-->OK",vals)

          #.keys()
print("alle auswählbaren keys=",vals)
#print(obj.scan_values("xwerte","$.[*].value"))
#print(obj.scan_values("xwerte","$.features[*].geometry.coordinates"))
#print(obj.scan_values("ywerte","$.features[*].geometry.coordinates[0]"))
#print(obj.scan_values("magwerte","$.features[*].properties.mag"))

v1=obj.find_possible_keypath("2")#[]#stringency_index[0]")
print("keyname=",v1)
if v1 != "":
     v2= obj.scan_values("sdf", v1)#+"[0]")
     print(v1, "-scan=",type(v2), "=>", v2)
     v2= obj.get_values("sdf")#+"[0]")
     print(v1, "-getval=",type(v2), "=>", v2)

#x = obj.get_values("xwerte")
# print("-->",x)
# print("-->",obj.get_values("ywerte"))
# print("-->",obj.get_values("magwerte"))
# for match in x:
#     print(f'Employee id: {match.value}')
#print(match.value)
#print("id value is", match[0].value)

