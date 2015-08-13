# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TEQUIP(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		for key, val in self.items():
			return {"dbid" : val[0], "eid" : val[1]}

	def createFromDict(self, dictData):
		self[dictData["dbid"]] = [dictData["dbid"], dictData["eid"]]
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