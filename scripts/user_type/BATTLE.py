# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *

class TBATTLE_ENEMY(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "enemyid": self[1],
            "def": self[2],
            "health": self[3],
            "maxhealth": self[4],
            "dodge": self[5],
            "attack":self[6],
            "exp":self[7],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"],
                     dictData["enemyid"],
                     dictData["def"],
                     dictData["health"],
                     dictData["maxhealth"],
                     dictData["dodge"],
                     dictData["attack"],
                     dictData["exp"]])
        return self


class BATTLE_ENEMY_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TBATTLE_ENEMY().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TBATTLE_ENEMY)


enemy_inst = BATTLE_ENEMY_PICKLER()


######################################################################################################

class TBATTLE_OP(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "from": self[0],
            "to": self[1],
            "itemid": self[2],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["from"], dictData["to"], dictData["itemid"]])
        return self


class BATTLE_OP_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TBATTLE_OP().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TBATTLE_OP)


op_inst = BATTLE_OP_PICKLER()

######################################################################################################

class TBATTLE_OBJ(list):
    def __init__(self):
        list.__init__(self)

    def asDict(self):
        data = {
            "dbid": self[0],
            "health": self[1],
        }

        return data

    def createFromDict(self, dictData):
        self.extend([dictData["dbid"], dictData["health"]])
        return self


class BATTLE_OBJ_PICKLER:
    def __init__(self):
        pass

    def createObjFromDict(self, dct):
        return TBATTLE_OBJ().createFromDict(dct)

    def getDictFromObj(self, obj):
        return obj.asDict()

    def isSameType(self, obj):
        return isinstance(obj, TBATTLE_OBJ)


bo_inst = BATTLE_OBJ_PICKLER()