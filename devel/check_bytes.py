from libpyvinyl.Parameters.Collections import CalculatorParameters


p = CalculatorParameters()
p.new_parameter("str1")
p["str1"] = 'customized string1'
print(p)
# this is OK
p.to_json("test_bytes1.json")


# now the string is encoded to a bytes object
p = CalculatorParameters()
p.new_parameter("str2")
p["str2"] = 'customized string2'.encode('UTF-8') # or just  p["str2"] = b'custimized string'
print(p)
# this falis
# p.to_json("test_bytes2.json")



# now numpy bytes object
import numpy
p = CalculatorParameters()
p.new_parameter("test3")
p["test3"] = numpy.array([1,2,3]).tobytes()
print(p)
# this falis
# p.to_json("test_bytes3.json")