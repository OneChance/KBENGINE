# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TBGGRID(list):

	def __init__(self):
		list.__init__(self)

	def asDict(self):
		data = {
			"dbid": self[0],
			"iid": self[1],
			"num": self[2],
			"level": self[3],
			"commontype": self[4],
			"stamina" : self[5],
			"maxstamina" : self[6],
			"health" : self[7],
			"maxhealth" : self[8],
			"strength" : self[9],
			"archeology" : self[10],
			"def" : self[11],
			"dodge" : self[12],
			"exp" : self[13],
			"digpower" : self[14],
			"attack" : self[15],
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["iid"],dictData["num"],dictData["level"],dictData["commontype"],dictData["stamina"],
					 dictData["maxstamina"],dictData["health"],dictData["maxhealth"],dictData["strength"],dictData["archeology"],
					 dictData["def"],dictData["dodge"],dictData["exp"],dictData["digpower"],dictData["attack"]])
		return self
		
class BGGRID_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TBGGRID().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TBGGRID)

bggrid_inst = BGGRID_PICKLER()