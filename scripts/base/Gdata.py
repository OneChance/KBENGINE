# -*- coding: utf-8 -*-
import KBEngine
from ROLE import TROLE
from BATTLEOBJ import TBATTLEOBJ
from PLAYER import TPLAYER
from KBEDebug import *
from ITEM import TITEMList

class Gdata(KBEngine.Proxy):

	global DATAVERSION;

	def __init__(self):
		KBEngine.Proxy.__init__(self)
		self.accountEntity = None

	def reqItemList(self,data_version):
		"""
		exposed.
		客户端请求查询道具列表
		"""
		self.DATAVERSION = data_version
		gdata = KBEngine.createBaseFromDBID("Gdata",1,self.onGetData);

	def onGetData(self, baseRef, dbid, wasActive):
		gdataEntity = KBEngine.entities.get(baseRef.id);
		if(self.DATAVERSION < gdataEntity.version):
			self.client.onReqItemList(self.items)
		else:
			self.client.onReqItemList(TITEMList())
		self.giveClientTo(self.accountEntity)
		
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
		INFO_MSG("gdata[%i] entities enable. mailbox:%s" % (self.id, self.client))
			
	def onLogOnAttempt(self, ip, port, password):
		"""
		KBEngine method.
		客户端登陆失败时会回调到这里
		"""
		INFO_MSG(ip, port, password)
		return KBEngine.LOG_ON_ACCEPT
		
	def onClientDeath(self):
		"""
		KBEngine method.
		客户端对应实体已经销毁
		"""
		DEBUG_MSG("gdata[%i].onClientDeath:" % self.id)
		self.accountEntity.destroy()
		self.accountEntity = None
		self.destroy()
