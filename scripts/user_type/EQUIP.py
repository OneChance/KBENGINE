# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TEQUIP(list):
	"""
	"""
	def __init__(self):
		list.__init__(self)

	def asDict(self):
		data = {
			"dbid": self[0],
			"iid": self[1],
			"level": self[2],
			"commontype": self[3],
		}

		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["iid"],dictData["level"],dictData["commontype"]])
		return self
		
class EQUIP_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TEQUIP().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TEQUIP)

inst = EQUIP_PICKLER()