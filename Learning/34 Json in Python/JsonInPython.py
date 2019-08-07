# JsonInPython
# Play with JSON in Python
# https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
# 2018-03-13    PV

# json.dumps(obj, ...) : Serialize obj to a JSON formatted str
# json.loads(s, ...) : Deserialize a JSON formatted object to a python object
# json.dump(obj, fileobject, ..) : Serialize obj as a JSON formatted stream to
# file
# json.load(fileobject, ...  ) : Deserialize a file-like object containing JSON

# use jsonpickle Python library for serialization/deserialization of complex
# Python objects to and from JSON

import json


simple_list = [42, "Hello", True, 3.14]
s = json.dumps(simple_list)
print(s)

simple_list_2 = json.loads(s)
print(simple_list_2)



class Detail(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class RootConfig(object):
    def __init__(self):
        self.i = 12
        self.s = "RootConfig variable s"
        self.l = [2,3,5,7,11]
        self.d = {1:'one', 2:'two', 3:'three'}
        self.dl = [Detail(1,"A"), Detail(2,"B"), Detail(Detail(31, "C1"), Detail(32, 'C2'))]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


# Use json.dumps in a serializer method implemented as a public member of the class to serialize
rc = RootConfig()
t = rc.toJSON()
print(t, '\n\n')



# Extend JSONEncoder
class MyEncoder(json.JSONEncoder):
    def default(self, o):
        return o.__dict__

u = MyEncoder().encode(rc)
print(u)
