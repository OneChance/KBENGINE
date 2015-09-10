# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *


class TVECTOR(dict):
    def __init__(self):
        dict.__init__(self)

    def asDict(self):
        for key, val in self.items():
            return {"x": val[0],
                    "y": val[1],
                    "z": val[2]}

    def createFromDict(self, dictData):
        self[0] = [dictData["x"], dictData["y"], dictData["z"]]
        return self


class VECTOR_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TVECTOR().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TVECTOR)


vector_inst = VECTOR_PICKLER()


######################################################################################################

class TELEMENTDATA(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "vecs": self[1],
            "objname": self[2],
            "order": self[3],
            "dig_deep": self[4],
            "dig_currentDeep": self[5],
            "dig_texture": self[6],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"], dictData["vecs"], dictData["objname"], dictData["order"],dictData["dig_deep"],
                     dictData["dig_currentDeep"],dictData["dig_texture"]])
        return self


class ELEMENTDATA_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TELEMENTDATA().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TELEMENTDATA)


elementdata_inst = ELEMENTDATA_PICKLER()


######################################################################################################


class TFLOOR(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "grounds": self[1],
            "gitems": self[2],
            "genemys": self[3],
            "gdigs": self[4],
            "entrys": self[5],
            "digtonextpos": self[6],
            "istomb": self[7],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"], dictData["grounds"], dictData["gitems"], dictData["genemys"], dictData["gdigs"],
                     dictData["entrys"], dictData["digtonextpos"], dictData["istomb"]])
        return self


class FLOOR_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TFLOOR().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TFLOOR)


floor_inst = FLOOR_PICKLER()


######################################################################################################



######################################################################################################

class TTOMB(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "floors": self[1],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"], dictData["floors"]])
        return self


class TOMB_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TTOMB().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TTOMB)


tomb_inst = TOMB_PICKLER()


######################################################################################################

class TTOMBINFO(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "level": self[1],
            "name": self[2],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"], dictData["level"], dictData["name"]])
        return self


class TOMBINFO_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TTOMBINFO().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TTOMBINFO)


tombinfo_inst = TOMBINFO_PICKLER()


######################################################################################################

class TTOMBINFOList(dict):
    """
    """

    def __init__(self):
        """
        """
        dict.__init__(self)

    def asDict(self):
        datas = []
        dct = {"values": datas}

        for key, val in self.items():
            datas.append(val)

        return dct

    def createFromDict(self, dictData):
        for data in dictData["values"]:
            self[data[0]] = data
        return self


class TOMBINFO_LIST_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TTOMBINFOList().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TTOMBINFOList)


tombinfo_list_inst = TOMBINFO_LIST_PICKLER()


###############################################################################################


