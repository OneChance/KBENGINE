# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TBGGRID(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		for key, val in self.items():
			return {"dbid" : val[0], "iid" : val[1],"num" : val[2],"ilevel" : val[3]}

	def createFromDict(self, dictData):
		self[dictData["dbid"]] = [dictData["dbid"], dictData["iid"],dictData["num"],dictData["ilevel"]]
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

inst = BGGRID_PICKLER()