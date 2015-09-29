# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TPLAYER(dict):

	def __init__(self):
		dict.__init__(self)
		
	def asDict(self):
		for key, val in self.items():
			return {"name":val[0],
					"stamina" : val[1],
					"maxstamina" : val[2],
					"health" : val[3],
					"maxhealth" : val[4],
					"strength" : val[5],
					"archeology" : val[6],
					"def" : val[7],
					"dodge" : val[8],
					"level" : val[9],
					"exp" : val[10],
					"digpower" : val[11],
					"pro" : val[12],
					"img" : val[13],
					"attack" : val[14],
					"teamid" : val[15],
					"isleader" : val[16]}

	def createFromDict(self, dictData):
		self[0] = [dictData["name"],
				   dictData["stamina"],
				   dictData["maxstamina"],
				   dictData["health"],
				   dictData["maxhealth"],
				   dictData["strength"],
				   dictData["archeology"],
				   dictData["def"],
				   dictData["dodge"],
				   dictData["level"],
				   dictData["exp"],
				   dictData["digpower"],
				   dictData["pro"],
				   dictData["img"],
				   dictData["attack"],
				   dictData["teamid"],
				   dictData["isleader"]]
		return self
		
class PLAYER_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TPLAYER().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TPLAYER)

inst = PLAYER_PICKLER()