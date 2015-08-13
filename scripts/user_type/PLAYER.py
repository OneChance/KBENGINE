# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TPLAYER(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		for key, val in self.items():
			return {"iid" : val[0],"name":val[1],"stamina" : val[2], "health" : val[3],"level" : val[4],"exp" : val[5]}

	def createFromDict(self, dictData):
		self[0] = [dictData["iid"],dictData["name"],dictData["stamina"], dictData["health"],dictData["level"],dictData["exp"]]
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