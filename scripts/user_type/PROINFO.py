from KBEDebug import *

class pro:

    strengthFactor = 0
    archeologyFactor = 0
    defFactor = 0
    dodgeFactor = 0
    healthFactor = 0
    staminaFactor = 0
    attack = 0
    digPower = 0

    def __init__(self,strengthFactor,archeologyFactor,defFactor,dodgeFactor,healthFactor,staminaFactor):
	    self.strengthFactor = strengthFactor
	    self.archeologyFactor = archeologyFactor
	    self.defFactor = defFactor
	    self.dodgeFactor = dodgeFactor
	    self.healthFactor = healthFactor
	    self.staminaFactor = staminaFactor

class Geomancer(pro):
	def __init__(self):
		pro.__init__(self,2,10,2,1,10,30)
	def setInfo(self,strength):
		self.attack = strength
		self.digPower = strength

class Settler(pro):
	def __init__(self):
		pro.__init__(self,6,0,10,3,30,50)
	def setInfo(self,strength):
		self.attack = strength * 2
		self.digPower = strength * 4

class Doctor(pro):
	def __init__(self):
		pro.__init__(self,2,0,5,2,20,30)
	def setInfo(self,strength):
		self.attack = strength
		self.digPower = strength

class Exorcist(pro):
	def __init__(self):
		pro.__init__(self,5,0,8,10,20,20)
	def setInfo(self,strength):
		self.attack = strength * 4
		self.digPower = strength

class ProFactory:
	@staticmethod
	def getPro(proname,gdata,iid):

		if(iid>0):
			assitInfo = gdata.items[iid]
			proname = assitInfo.asDict()["pro"]

		pro = ProFactory.getProType(proname)

		if(pro != None and iid >0):
			pro.healthFactor = assitInfo.asDict()["health"]
			pro.staminaFactor = assitInfo.asDict()["stamina"]
			pro.strengthFactor = assitInfo.asDict()["strength"]
			pro.archeologyFactor = assitInfo.asDict()["archeology"]
			pro.defFactor = assitInfo.asDict()["def"]
			pro.dodgeFactor = assitInfo.asDict()["dodge"]

		return pro

	@staticmethod
	def getProType(proname):

		if(proname == 'Geomancer'):
			return Geomancer()
		elif(proname == 'Settler'):
			return Settler()
		elif(proname == 'Doctor'):
			return Doctor()
		elif(proname == 'Exorcist'):
			return Exorcist()
		else:
			return None
