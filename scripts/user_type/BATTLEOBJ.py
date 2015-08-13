# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TBATTLEOBJ(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		for key, val in self.items():
			return {"dbid" : val[0], "iid" : val[1],"info" : val[2]}

	def createFromDict(self, dictData):
		self[dictData["dbid"]] = [dictData["dbid"], dictData["iid"],dictData["info"]]
		return self
		
class BATTLEOBJ_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TBATTLEOBJ().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TBATTLEOBJ)

inst = BATTLEOBJ_PICKLER()