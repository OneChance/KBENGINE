# -*- coding: utf-8 -*-
import KBEngine
from ROLE import TROLE
from BATTLEOBJ import TBATTLEOBJ
from PLAYER import TPLAYER
from KBEDebug import *
from Gdata import *
from ITEM import *
from BGGRID import *
from PROINFO import *

class Account(KBEngine.Proxy):

	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.gdata = None

	def reqRoleList(self):
		"""
		exposed.
		客户端请求查询角色列表
		"""
		DEBUG_MSG("Account[%i].reqRoleList: size=%i." % (self.id, len(self.roles)))

		if(len(self.roles)>0):
			self.setBgDBID()
		self.client.onReqRoleList(self.roles)
		gdata = KBEngine.createBaseAnywhereFromDBID("Gdata",1,self.onGetData)


	def onGetData(self, baseRef, dbid, wasActive):
		gdataEntity = KBEngine.entities.get(baseRef.id)
		gdataEntity.accountEntity = self
		self.gdata = gdataEntity
		self.giveClientTo(gdataEntity)


	def reqCreateRole(self, name,pro):
			role = TROLE()
			playerInfoDict = {"name":name,
							  "stamina" : 0,
							  "maxstamina" : 0,
							  "health" : 0,
							  "maxhealth" : 0,
							  "strength" : 0,
							  "archeology" : 0,
							  "def" : 0,
							  "dodge" : 0,
							  "level" : 0,
							  "exp" : 0,
							  "digpower" : 0,
							  "pro" : pro,
						      "img" : 1,
							  "attack":0}

			self.addExp(playerInfoDict,0,[],401)
			player = TPLAYER().createFromDict(playerInfoDict)
			role.extend([0,player,[],[],[],5000])
			self.roles[0] = role


			self.writeToDB()
			self.client.onCreateRoleResult(role)


	def addExp(self,playerInfoDict,exp,equips,iid):

		level = playerInfoDict["level"]
		playerInfoDict["exp"] =  playerInfoDict["exp"] + exp
		res = self.expLevel(playerInfoDict["exp"],level)

		if(res["level"]>level):
			playerInfoDict["level"] = res["level"]
			self.levelUp(playerInfoDict,equips,iid)


	def expLevel(self,exp,level):
		nextExp = level * 50;

		if (exp >= nextExp):
			level += 1
			return self.expLevel (exp - nextExp, level)
		else:
			return {"exp":exp,"level":level}

	def levelUp(self,playerInfoDict,equips,iid):
		self.attrUpdate(playerInfoDict,equips,iid)


	def attrUpdate(self,playerInfoDict,equips,iid):

		pro = ProFactory.getPro(playerInfoDict["pro"],self.gdata,iid)

		level = playerInfoDict["level"]

		playerInfoDict["health"] = level * pro.healthFactor
		playerInfoDict["maxhealth"] = level * pro.healthFactor
		playerInfoDict["stamina"] = level * pro.staminaFactor
		playerInfoDict["maxstamina"] = level * pro.staminaFactor
		playerInfoDict["strength"] = level * pro.strengthFactor
		playerInfoDict["archeology"] = level * pro.archeologyFactor
		playerInfoDict["def"] = level * pro.defFactor
		playerInfoDict["dodge"] = level * pro.dodgeFactor
		pro.setInfo(playerInfoDict["strength"])
		playerInfoDict["attack"] = pro.attack
		playerInfoDict["digPower"] = pro.digPower


		if(len(equips)>0):
			for equip in equips:
				ERROR_MSG("test")

	def tradeItem(self,iid,tradeType,num,dbid,level):

			traderes = "ok"
			iList = self.gdata.items
			roleMoney = self.roles[0].asDict()["money"]

			if(iList is not None):

				haveItem = False

				for key in iList:
					if(key == iid):
						haveItem = True

				if(haveItem):
					price = iList[iid].asDict()["price"]

					if(tradeType==0):

						tradeMoney = price * num;
						if(roleMoney>=tradeMoney):
							roleMoney -= tradeMoney

							addmsg = self.addItem(iList[iid].asDict(),num,level)

							if(addmsg != "ok"):
								traderes = addmsg
							else:
								self.roles[0][5] = roleMoney
								self.writeToDB()
						else:
							traderes = "NOTENOUGHMONEY"
					else:

						tradeMoney = (int)(price * 0.5 * level)  * num;

						roleMoney += tradeMoney

						addmsg = self.removeItem(iList[iid].asDict(),num,dbid)

						if(addmsg != "ok"):
							traderes = addmsg
						else:
							self.bgSameCombine()
							self.roles[0][5] = roleMoney
							self.writeToDB()
				else:
					traderes = "NOMATCHITEM"
			else:
				traderes = "NOITEMLIST"

			self.setBgDBID()
			self.client.onTradeOver(self.roles[0],traderes)

	def setBgDBID(self):
		bggrids = self.roles[0][3]
		for i in range(0, len(bggrids)):
			 bggrids[i][0] = i

	def bgSameCombine(self):

		bggrids_notCombine = []
		bggrids = self.roles[0][3]

		dif_type = {}
		for i in range(0, len(bggrids)):
			bagInfo = bggrids[i]
			"""装备和雇佣兵卡片不叠加"""
			if(bagInfo[4] != 1 and bagInfo[4]!=2):
				if bagInfo[1] in dif_type:
					dif_type[bagInfo[1]][2] = dif_type[bagInfo[1]][2] + bagInfo[2]
				else:
					dif_type[bagInfo[1]] = bagInfo
			else:
				bggrids_notCombine.append(bagInfo)

		bggrids = []
		bggrids = bggrids_notCombine

		for key in dif_type:
			self.setBg(bggrids,key,dif_type[key])

		self.roles[0][3] = bggrids

	def setBg(self,bggrids,iid,bag_info):
		grid = TBGGRID()
		if(bag_info[2]>99):
			grid.extend([0,iid,99,bag_info[3],bag_info[4]])
			bggrids.append(grid)
			bag_info[2] = bag_info[2] - 99
			self.setBg(bggrids,iid,bag_info)
		else:
			bggrids.append(bag_info)

	def addItem (self,item,tradeNum,level):

		"""
		:param item: 要买入的道具信息
		:param num: 数量
		:return:
		"""

		"""该角色道具列表"""
		bggrids = self.roles[0][3]

		needToAdd = True

		if (item["commontype"] == 1 or item["commontype"] == 2):

			if(len(bggrids)+tradeNum > 16):
				return "NUMOVER"
			else:
				for i in range(0, tradeNum):
					grid = TBGGRID()
					grid.extend([0,item["dbid"],1,level,item["commontype"]])
					bggrids.append(grid)


		else:
			"""消耗品堆叠数量不能超过99"""
			for i in range(0, len(bggrids)):

				bagInfo = bggrids[i]

				if (bagInfo[1] == item["dbid"]):

					if (bagInfo[2] == 99):
						continue

					bagInfo[2] += tradeNum;

					if (bagInfo[2] > 99):
						tradeNum = bagInfo[2] - 99
						bagInfo[2] = 99
						needToAdd = True
					else:
						needToAdd = False

			if (needToAdd):
				grid = TBGGRID()
				grid.extend([0,item["dbid"],tradeNum,level,item["commontype"]])

				if(len(bggrids) == 16):
					return "NUMOVER"

				bggrids.append(grid)

		return "ok"

	def removeItem (self,item,tradeNum,dbid):

		"""
		:param item: 要卖出的道具信息
		:param num: 数量
		:param dbid: 要买出的道具的背包格子的id
		:return:
		"""

		"""该角色道具列表"""
		bggrids = self.roles[0][3]

		if (item["commontype"] == 1 or item["commontype"] == 2):

			for i in range(0, len(bggrids)):
				bagInfo = bggrids[i]
				if (bagInfo[1] == item["dbid"]):
					bggrids.remove(bagInfo)
					break


		else:

			bagInfo = bggrids[dbid]
			bagInfo[2] -= tradeNum;

			if(bagInfo[2]==0):
				bggrids.remove(bagInfo)

		return "ok"

	def onTimer(self, id, userArg):
		"""
		KBEngine method.
		使用addTimer后， 当时间到达则该接口被调用
		@param id		: addTimer 的返回值ID
		@param userArg	: addTimer 最后一个参数所给入的数据
		"""
		DEBUG_MSG(id, userArg)
		
	def onEntitiesEnabled(self):


		"""
		KBEngine method.
		该entity被正式激活为可使用， 此时entity已经建立了client对应实体， 可以在此创建它的
		cell部分。
		"""
		INFO_MSG("account[%i] entities enable. mailbox:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)

		if self.gdata:
			self.gdata.giveClientTo(self)
			self.gdata.destroySelf()
			self.gdata = None

		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("Account[%i].onClientDeath:" % self.id)
		self.destroy()
