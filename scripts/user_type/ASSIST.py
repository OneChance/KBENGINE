# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TASSIST(list):

	def __init__(self):
		list.__init__(self)

	def asDict(self):
		data = {
			"dbid": self[0],
			"stamina" : self[1],
			"maxstamina" : self[2],
			"health" : self[3],
			"maxhealth" : self[4],
			"iid": self[5],     #如果是玩家,这个字段放置img
			"level": self[6],
			"commontype": self[7],
			"strength" : self[8],
			"archeology" : self[9],
			"def" : self[10],
			"dodge" : self[11],
			"exp" : self[12],
			"digpower" : self[13],
			"attack" : self[14],
			"player" : self[15],
			"playername" : self[16],
			"playerpro" : self[17],
			"playerid" : self[18],
			"onlinestate" : self[19],
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["stamina"],dictData["maxstamina"],dictData["health"],dictData["maxhealth"],
					 dictData["iid"],dictData["level"],dictData["commontype"],dictData["strength"],dictData["archeology"],
					 dictData["def"],dictData["dodge"],dictData["exp"],dictData["digpower"],dictData["attack"],
					 dictData["player"],dictData["playername"],dictData["playerpro"],dictData["playerid"],
					 dictData["onlinestate"]])
		return self
		
class ASSIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TASSIST().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TASSIST)

assist_inst = ASSIST_PICKLER()