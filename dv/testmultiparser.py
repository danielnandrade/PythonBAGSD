
import multiparser as js

##########################################################################
############     EXAMPLE ILLUSTRATION OF MULTIPARSER           ###########
##########################################################################

# Sources
obj = js.MultiParser(filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/eq_data_1_day_m1.jsonx")
#obj = js.multiParser(url="https://covid.ourworldindata.org/data/owid-covid-data.json")
#obj = js.multiParser(filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/owid-covid-data_deu.json")
#obj = js.multiParser(filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/kap_13_Pegel_Bonn.json")


print("alle auswählbaren keys=",list(obj.find_possible_keynames_all().keys()))
#print(obj.scan_values("xwerte","$.[*].value"))
#print(obj.scan_values("xwerte","$.features[*].geometry.coordinates"))
#print(obj.scan_values("ywerte","$.features[*].geometry.coordinates[0]"))
#print(obj.scan_values("magwerte","$.features[*].properties.mag"))

v1=obj.find_possible_keypath("coordinates")#[]#stringency_index[0]")
print("keyname=",v1)
if v1 != "":
     v2= obj.scan_values("sdf", v1)#+"[0]")
     print(v1, "=",type(v2), "=>", v2)
     v2= obj.get_values("sdf")#+"[0]")
     print(v1, "=",type(v2), "=>", v2)

#x = obj.get_values("xwerte")
# print("-->",x)
# print("-->",obj.get_values("ywerte"))
# print("-->",obj.get_values("magwerte"))
# for match in x:
#     print(f'Employee id: {match.value}')
#print(match.value)
#print("id value is", match[0].value)

