# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TSHOPITEM(list):
	"""
	"""
	def __init__(self):
		"""
		"""
		list.__init__(self)
		
	def asDict(self):
		data = {
			"dbid": self[0],
			"iid": self[1],
		}
		
		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["iid"]])
		return self
		
class SHOPITEM_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TSHOPITEM().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TSHOPITEM)

shopitem_inst = SHOPITEM_PICKLER()

class TSHOPITEMList(dict):
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
		
class SHOPITEM_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TSHOPITEMList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TSHOPITEMList)

shopitem_list_inst = SHOPITEM_LIST_PICKLER()