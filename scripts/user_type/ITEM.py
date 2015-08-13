# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import * 

class TITEM(list):
	"""
	"""
	def __init__(self):
		"""
		"""
		list.__init__(self)
		
	def asDict(self):
		data = {
			"dbid": self[0],
			"name": self[1],
			"usetype": self[2],
			"rangetype": self[3],
			"commontype": self[4],
			"objtype": self[5],
			"prefabname": self[6],
			"note": self[7],
			"targetnote": self[8],
			"price": self[9],
			"strength": self[10],
			"archeology": self[11],
			"def": self[12],
			"dodge": self[13],
			"epos": self[14],
			"level": self[15],
			"stamina": self[16],
			"pro": self[17],
			"levelexpadd": self[18],
			"attack": self[19],
		}
		
		return data

	def createFromDict(self, dictData):
		self.extend([dictData["dbid"],dictData["name"],dictData["usetype"],dictData["rangetype"],dictData["commontype"],
					 dictData["objtype"],dictData["prefabname"],dictData["note"],dictData["targetnote"],
					 dictData["price"],dictData["strength"],dictData["archeology"],dictData["def"],dictData["dodge"],
					 dictData["epos"],dictData["level"],dictData["stamina"],dictData["pro"],dictData["levelexpadd"],dictData["attack"]])
		return self
		
class ITEM_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TITEM().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TITEM)

item_inst = ITEM_PICKLER()

class TITEMList(dict):
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
		
class ITEM_LIST_PICKLER:
	def __init__(self):
		pass

	def createObjFromDict(self, dct):
		return TITEMList().createFromDict(dct)

	def getDictFromObj(self, obj):
		return obj.asDict()

	def isSameType(self, obj):
		return isinstance(obj, TITEMList)

item_list_inst = ITEM_LIST_PICKLER()