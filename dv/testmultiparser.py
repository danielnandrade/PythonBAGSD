
import multiparser as js

obj = js.multiParser(filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/eq_data_1_day_m1.json")
#obj = js.multiParser(filename="C:/Users/Nebil/Desktop/DataScientist/PycharmProjects/pythonProject1/owid-covid-data_deu.json")

#print("alle auswählbaren keys=",list(obj.find_possible_keynames_all().keys()))
#print(obj.scan_values("xwerte","$.features[*].geometry.coordinates"))
#print(obj.scan_values("ywerte","$.features[*].geometry.coordinates[1]"))
#print(obj.scan_values("magwerte","$.features[*].properties.mag"))

v=obj.find_possible_keypath("coordinates[1]")#[]#stringency_index[0]")
print("keyname=",v)
if v != "":
     print(v, "=",obj.scan_values("sdf",v)[0:5])


#x = obj.get_values("xwerte")
# print("-->",x)
# print("-->",obj.get_values("ywerte"))
# print("-->",obj.get_values("magwerte"))
# for match in x:
#     print(f'Employee id: {match.value}')
#print(match.value)
#print("id value is", match[0].value)

