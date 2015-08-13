# -*- coding: utf-8 -*-
import KBEngine
from ROLE import TROLE
from BATTLEOBJ import TBATTLEOBJ
from PLAYER import TPLAYER
from KBEDebug import *
from Gdata import *

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
		self.client.onReqRoleList(self.roles)
		gdata = KBEngine.createBaseAnywhereFromDBID("Gdata",1,self.onGetData);


	def onGetData(self, baseRef, dbid, wasActive):
		gdataEntity = KBEngine.entities.get(baseRef.id);
		gdataEntity.accountEntity = self
		self.gdata = gdataEntity;
		self.giveClientTo(gdataEntity)


	def reqCreateRole(self, name,pro):
			role = TROLE()
			player = TPLAYER().createFromDict({"name":name,"stamina" : 0, "health" :0, "level" :1,"iid":(int)(pro)})
			role.extend([0,player,[],[],[]])
			self.roles[0] = role
			self.writeToDB()
		
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
