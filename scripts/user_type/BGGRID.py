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
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["iid"],dictData["num"],dictData["level"],dictData["commontype"]])
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