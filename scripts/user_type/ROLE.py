# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TROLE(list):
	"""
	"""
	def __init__(self):
		"""
		"""
		list.__init__(self)
		
	def asDict(self):
		data = {
			"dbid": self[0],
			"info": self[1],
		    "equips": self[2],
			"bggrids": self[3],
			"assists": self[4],
		    "money": self[5],
		    "tombs": self[6],
		}
		
		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["info"],dictData["equips"],dictData["bggrids"],dictData["assists"],dictData["money"],dictData["tombs"]])
		return self
		
class ROLE_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TROLE().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TROLE)

role_inst = ROLE_PICKLER()

class TROLEList(dict):
	"""
	"""
	def __init__(self):
		"""
		"""
		dict.__init__(self)
		
	def asDict(self):
		datas = []
		dct = {"values" : datas}

		for key, val in self.items():
			datas.append(val)
			
		return dct

	def createFromDict(self, dictData):
		for data in dictData["values"]:
			self[data[0]] = data
		return self
		
class ROLE_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TROLEList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TROLEList)

role_list_inst = ROLE_LIST_PICKLER()