# -*- coding: utf-8 -*-
import KBEngine
import random
from ROLE import TROLE
from ASSIST import *
from PLAYER import TPLAYER
from KBEDebug import *
from Gdata import *
from ITEM import *
from BGGRID import *
from PROINFO import *
from EQUIP import *
from ItemFactory import *
from BATTLE import *
from TEAM import *

import time


class Account(KBEngine.Proxy):

    global current_enemy

    current_enemy = 0

    def __init__(self):
        KBEngine.Proxy.__init__(self)
        self.gdata = None

    def reqRoleList(self):
        """
        exposed.
        客户端请求查询角色列表
        """
        if (len(self.roles) > 0):
            self.setBgDBID()
            self.setEquipDBID()
            self.setAssistDBID()

        #通知队友上线，并获得队友在线信息
        self.onLineNoti()
        self.client.onReqRoleList(self.roles)

        gdata = KBEngine.createBaseAnywhereFromDBID("Gdata", 1, self.onGetData)


    def toPreFloor(self,tombid):
        self.roles[0][10] = min(self.roles[0][10] - 1,1)

    def toNextFloor(self,tombid):
        self.roles[0][10] = self.roles[0][10] + 1

    def enterTomb(self,tombid):

        self.roles[0][9] = tombid
        self.roles[0][10] = 1

        self.client.onEnterTomb(tombid)


    def onGetData(self, baseRef, dbid, wasActive):
        gdataEntity = KBEngine.entities.get(baseRef.id)
        gdataEntity.accountEntity = self
        self.gdata = gdataEntity
        self.giveClientTo(gdataEntity)

    def reqCreateRole(self, name, pro):
        role = TROLE()

        playerInfoDict = {"name": name,
                          "stamina": 0,
                          "maxstamina": 0,
                          "health": 0,
                          "maxhealth": 0,
                          "strength": 0,
                          "archeology": 0,
                          "def": 0,
                          "dodge": 0,
                          "level": 0,
                          "exp": 0,
                          "digpower": 0,
                          "pro": pro,
                          "img": 1,
                          "attack": 0,
                          "teamid": 0,
                          "isleader": 0,
                          "scenelevel": 2}

        self.addExp(playerInfoDict, 0, [], 0)
        player = TPLAYER().createFromDict(playerInfoDict)
        role.extend([0, player, [], [], [], 5000, [],[],[],0,0])
        self.roles[0] = role

        self.writeToDB()
        self.client.onCreateRoleResult(role)

    def addExp(self, playerInfoDict, exp, equips, iid):

        level = playerInfoDict["level"]
        playerInfoDict["exp"] = playerInfoDict["exp"] + exp
        res = self.expLevel(playerInfoDict["exp"], level)

        if (res["level"] > level):
            playerInfoDict["exp"] = res["exp"]
            playerInfoDict["level"] = res["level"]
            self.levelUp(playerInfoDict, equips, iid)

    def expLevel(self, exp, level):
        nextExp = level * 50;

        if (exp >= nextExp):
            level += 1
            return self.expLevel(exp - nextExp, level)
        else:
            return {"exp": exp, "level": level}

    def levelUp(self, playerInfoDict, equips, iid):
        self.attrUpdate(playerInfoDict, equips, iid)
        playerInfoDict["health"] = playerInfoDict["maxhealth"]
        playerInfoDict["stamina"] = playerInfoDict["maxstamina"]

    def attrUpdate(self, playerInfoDict, equips, iid):

        iList = self.gdata.items

        proname = ""

        if(iid==0):
            proname = playerInfoDict["pro"]

        pro = ProFactory.getPro(proname, self.gdata, iid)

        level = playerInfoDict["level"]

        playerInfoDict["maxhealth"] = level * pro.healthFactor
        playerInfoDict["maxstamina"] = level * pro.staminaFactor
        playerInfoDict["strength"] = level * pro.strengthFactor
        playerInfoDict["archeology"] = level * pro.archeologyFactor
        playerInfoDict["def"] = level * pro.defFactor
        playerInfoDict["dodge"] = level * pro.dodgeFactor

        if (len(equips) > 0):
            for equip in equips:
                equipInfo = iList[equip[1]]
                playerInfoDict["maxhealth"] = playerInfoDict["maxhealth"] + equipInfo.asDict()["health"]
                playerInfoDict["maxstamina"] = playerInfoDict["maxstamina"] + equipInfo.asDict()["stamina"]
                playerInfoDict["strength"] = playerInfoDict["strength"] + equipInfo.asDict()["strength"]
                playerInfoDict["archeology"] = playerInfoDict["archeology"] + equipInfo.asDict()["archeology"]
                playerInfoDict["def"] = playerInfoDict["def"] + equipInfo.asDict()["def"]
                playerInfoDict["dodge"] = playerInfoDict["dodge"] + equipInfo.asDict()["dodge"]

        pro.setInfo(playerInfoDict["strength"])

        playerInfoDict["attack"] = pro.attack
        playerInfoDict["digpower"] = pro.digPower

        if (playerInfoDict["health"] > playerInfoDict["maxhealth"]):
            playerInfoDict["health"] = playerInfoDict["maxhealth"]

        if (playerInfoDict["stamina"] > playerInfoDict["maxstamina"]):
            playerInfoDict["stamina"] = playerInfoDict["maxstamina"]

        return playerInfoDict

    def fromTagExplain(self,fromTag):
        ass = self.roles[0][4]
        enemyList = self.roles[0][7]
        dbid = int(fromTag)

        if (dbid == 1):
            fromBo = self.roles[0][1]
        elif (dbid < 5):
            for i in range(0, len(ass)):
                if (ass[i].asDict()["dbid"] == dbid):
                    fromBo = ass[i]
                    break
        else:
            for i in range(0, len(enemyList)):
                if (enemyList[i].asDict()["dbid"] == dbid):
                    fromBo = enemyList[i]
                    break

        return fromBo


    def toTagExplain(self, toTag):
        toList = []
        ass = self.roles[0][4]
        enemyList = self.roles[0][7]

        if(toTag != ""):
            if (toTag == 'ALLTEAM'):
                toList.append(self.roles[0][1])  # roles[0]->role   role[1]->player  player[0]->playerDict
                for i in range(0, len(ass)):
                    toList.append(ass[i])
            elif (toTag == 'ALLENEMY'):
                for i in range(0, len(enemyList)):
                    toList.append(enemyList[i])
            else:
                dbid = int(toTag)

                if (dbid == 1):
                    toList.append(self.roles[0][1])
                elif (dbid < 5):
                    for i in range(0, len(ass)):
                        if (ass[i].asDict()["dbid"] == dbid):
                            toList.append(ass[i])
                            break
                else:
                    for i in range(0, len(enemyList)):
                        if (enemyList[i].asDict()["dbid"] == dbid):
                            toList.append(enemyList[i])
                            break

        return toList

    def useItem(self, fromTag, toTag, dbid):
        iList = self.gdata.items
        bggrids = self.roles[0][3]
        useres = "ok"

        for i in range(0, len(bggrids)):
            bagInfo = bggrids[i]
            if (bagInfo[0] == dbid):
                itemInfo = iList[bagInfo[1]]

                fromBo = self.fromTagExplain(fromTag)
                toList = self.toTagExplain(toTag)

                ItemFactory.use(fromBo, toList, itemInfo)

                self.removeItem(itemInfo.asDict(), 1, dbid)
                self.writeToDB()
                self.client.onUseItemOver(self.roles[0], useres)
                break

    # 雇佣兵操作
    def assistOper(self, bg_dbid, ass_dbid):

        bggrids = self.roles[0][3]
        assists = self.roles[0][4]
        assistres = "ok"
        iList = self.gdata.items

        if (bg_dbid > 0):

            #如果已经组队，不允许NPC雇佣兵参战
            if(self.roles[0][1].asDict()["teamid"]>0):
                self.client.onAssistOperOver(TROLE(), "TEAMEDNOASSIST")
                return

            for i in range(0, len(bggrids)):
                bagInfo = bggrids[i]

                if (bagInfo[0] == bg_dbid):

                    assistInfo = iList[bagInfo[1]]
                    pro = assistInfo.asDict()["pro"]

                    if (pro != ''):

                        oldAssisToBag = None

                        for j in range(0, len(assists)):

                            oldAssist = assists[j]
                            assistDict = oldAssist.asDict()

                            if (oldAssist[0] == ass_dbid):
                                oldAssistInfo = iList[assistDict["iid"]]
                                oldAssisToBag = TBGGRID()

                                oldAssisToBag.extend([0, assistDict["iid"], 1, assistDict["level"], 2,
                                                      assistDict["stamina"], assistDict["maxstamina"],
                                                      assistDict["health"], assistDict["maxhealth"],
                                                      assistDict["strength"], assistDict["archeology"],
                                                      assistDict["def"], assistDict["dodge"],
                                                      assistDict["exp"], assistDict["digpower"],
                                                      assistDict["attack"]])

                                assists.remove(oldAssist)
                                break

                        assist = TASSIST()

                        bagInfoDict = bagInfo.asDict()

                        assist.extend(
                            [0, bagInfoDict["stamina"],
                             bagInfoDict["maxstamina"],
                             bagInfoDict["health"],
                             bagInfoDict["maxhealth"],
                             bagInfoDict["iid"],
                             bagInfoDict["level"],
                             bagInfoDict["commontype"],
                             bagInfoDict["strength"],
                             bagInfoDict["archeology"],
                             bagInfoDict["def"],
                             bagInfoDict["dodge"],
                             bagInfoDict["exp"],
                             bagInfoDict["digpower"],
                             bagInfoDict["attack"],0,"","",0,0])
                        assists.append(assist)
                        bggrids.remove(bagInfo)

                        if (oldAssisToBag != None):
                            bggrids.append(oldAssisToBag)

                    else:
                        assistres = "NOTASSIT"

                    break

        else:

            if (len(bggrids) == 16):
                assistres = "NUMOVER"
            else:
                for i in range(0, len(assists)):
                    assist = assists[i]
                    if (assist[0] == ass_dbid):
                        assists.remove(assist)
                        bggrid = TBGGRID()

                        assistDict = assist.asDict()

                        bggrid.extend([0, assistDict["iid"], 1, assistDict["level"], 2,
                                       assistDict["stamina"], assistDict["maxstamina"],
                                       assistDict["health"], assistDict["maxhealth"],
                                       assistDict["strength"], assistDict["archeology"],
                                       assistDict["def"], assistDict["dodge"],
                                       assistDict["exp"], assistDict["digpower"],
                                       assistDict["attack"]])
                        bggrids.append(bggrid)

        self.setBgDBID()
        self.setAssistDBID()

        if (assistres == 'ok'):
            self.writeToDB()

        self.client.onAssistOperOver(self.roles[0], assistres)

    def equipOper(self, dbid, operType):

        bggrids = self.roles[0][3]
        equips = self.roles[0][2]
        equipres = "ok"
        iList = self.gdata.items

        if (operType == 0):
            for i in range(0, len(bggrids)):
                bagInfo = bggrids[i]

                """获取背包中要装备的物品"""
                if (bagInfo[0] == dbid):

                    equipInfo = iList[bagInfo[1]]
                    epos = equipInfo.asDict()["epos"]

                    if (epos > 0):

                        oldEquip = None

                        """检查要换的位置有没有装备"""
                        for j in range(0, len(equips)):
                            oldEquipInfo = iList[equips[j][1]]
                            if (epos == oldEquipInfo.asDict()["epos"]):
                                oldEquip = TBGGRID()
                                oldEquip.extend(
                                    [0, equips[j][1], 1, equips[j][2], equips[j][3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                                equips.remove(equips[j])
                                break

                        equip = TEQUIP()
                        equip.extend([0, bagInfo[1], bagInfo[3], bagInfo[4]])
                        equips.append(equip)
                        bggrids.remove(bagInfo)

                        if (oldEquip != None):
                            bggrids.append(oldEquip)

                    else:
                        equipres = "NOTEQUIP"

                    break

        else:
            for i in range(0, len(equips)):
                equipInfo = equips[i]
                if (equipInfo[0] == dbid):
                    equips.remove(equipInfo)
                    bggrid = TBGGRID()
                    bggrid.extend([0, equipInfo[1], 1, equipInfo[2], equipInfo[3], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
                    bggrids.append(bggrid)
                    self.writeToDB()

        self.roles[0][1].createFromDict(self.attrUpdate(self.roles[0][1].asDict(), equips, 0))

        self.setEquipDBID()
        self.setBgDBID()

        if (equipres == 'ok'):
            self.writeToDB()

        self.client.onEquipOperOver(self.roles[0], equipres)


    #level:佣兵等级
    def tradeItem(self, iid, tradeType, num, dbid, level):

        traderes = "ok"
        iList = self.gdata.items
        roleMoney = self.roles[0].asDict()["money"]

        if (iList is not None):

            haveItem = False

            for key in iList:
                if (key == iid):
                    haveItem = True

            if (haveItem):
                price = iList[iid].asDict()["price"]

                if (tradeType == 0):

                    tradeMoney = price * num;
                    if (roleMoney >= tradeMoney):
                        roleMoney -= tradeMoney

                        addmsg = self.addItem(iList[iid].asDict(), num, level)

                        if (addmsg != "ok"):
                            traderes = addmsg
                        else:
                            self.roles[0][5] = roleMoney
                    else:
                        traderes = "NOTENOUGHMONEY"
                else:

                    tradeMoney = (int)(price * 0.5 * level) * num;

                    roleMoney += tradeMoney

                    addmsg = self.removeItem(iList[iid].asDict(), num, dbid)

                    if (addmsg != "ok"):
                        traderes = addmsg
                    else:
                        self.bgSameCombine()
                        self.roles[0][5] = roleMoney
            else:
                traderes = "NOMATCHITEM"
        else:
            traderes = "NOITEMLIST"

        self.setBgDBID()

        if (traderes == 'ok'):
            self.writeToDB()

        self.client.onTradeOver(self.roles[0], traderes)

    def setAssistDBID(self):

        assists = self.roles[0][4]
        for i in range(0, len(assists)):
            assists[i][0] = i + 2

    def setBgDBID(self):
        bggrids = self.roles[0][3]
        for i in range(0, len(bggrids)):
            bggrids[i][0] = i + 1

    def setEquipDBID(self):
        equips = self.roles[0][2]
        for i in range(0, len(equips)):
            equips[i][0] = i + 1

    def bgSameCombine(self):

        bggrids_notCombine = []
        bggrids = self.roles[0][3]

        dif_type = {}
        for i in range(0, len(bggrids)):
            bagInfo = bggrids[i]
            """装备和雇佣兵卡片不叠加"""
            if (bagInfo[4] != 1 and bagInfo[4] != 2):
                if bagInfo[1] in dif_type:
                    dif_type[bagInfo[1]][2] = dif_type[bagInfo[1]][2] + bagInfo[2]
                else:
                    dif_type[bagInfo[1]] = bagInfo
            else:
                bggrids_notCombine.append(bagInfo)

        bggrids = []
        bggrids = bggrids_notCombine

        for key in dif_type:
            self.setBg(bggrids, key, dif_type[key])

        self.roles[0][3] = bggrids

    """处理背包堆叠"""

    def setBg(self, bggrids, iid, bag_info):
        grid = TBGGRID()
        if (bag_info[2] > 99):
            grid.extend([0, iid, 99, bag_info[3], bag_info[4], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
            bggrids.append(grid)
            bag_info[2] = bag_info[2] - 99
            self.setBg(bggrids, iid, bag_info)
        else:
            bggrids.append(bag_info)

    def addItem(self, item, tradeNum, level):

        """
        :param item: 要买入的道具信息
        :param num: 数量
        :return:
        """

        """该角色道具列表"""
        bggrids = self.roles[0][3]

        needToAdd = True

        if (item["commontype"] == 1 or item["commontype"] == 2):

            if (len(bggrids) + tradeNum > 16):
                return "NUMOVER"
            else:
                for i in range(0, tradeNum):
                    grid = TBGGRID()

                    playerInfoDict = {"name": '',
                                      "stamina": 0,
                                      "maxstamina": 0,
                                      "health": 0,
                                      "maxhealth": 0,
                                      "strength": 0,
                                      "archeology": 0,
                                      "def": 0,
                                      "dodge": 0,
                                      "level": 1,
                                      "exp": 0,
                                      "digpower": 0,
                                      "pro": item["pro"],
                                      "img": 0,
                                      "attack": 0}

                    if (item["commontype"] == 2):
                        self.attrUpdate(playerInfoDict, [], item["dbid"])

                    grid.extend([0, item["dbid"], 1, level, item["commontype"], playerInfoDict["maxstamina"],
                                 playerInfoDict["maxstamina"], playerInfoDict["maxhealth"], playerInfoDict["maxhealth"],
                                 playerInfoDict["strength"], playerInfoDict["archeology"], playerInfoDict["def"],
                                 playerInfoDict["dodge"],
                                 playerInfoDict["exp"], playerInfoDict["digpower"], playerInfoDict["attack"]])

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
                grid.extend([0, item["dbid"], tradeNum, level, item["commontype"], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

                if (len(bggrids) == 16):
                    return "NUMOVER"

                bggrids.append(grid)

        return "ok"

    def removeItem(self, item, tradeNum, dbid):

        """
        :param item: 要卖出的道具信息
        :param num: 数量
        :param dbid: 要买出的道具的背包格子的id
        :return:
        """

        """该角色道具列表"""
        bggrids = self.roles[0][3]

        for i in range(0, len(bggrids)):
            bagInfo = bggrids[i]
            if (bagInfo[0] == dbid):
                bagInfo[2] -= tradeNum;
                if (bagInfo[2] == 0):
                    bggrids.remove(bagInfo)
                break

        return "ok"


    def getFloorInfoByTombIdFloorId(self,tomb_id,floor_id):

        tombs = self.roles[0][6]

        for i in range(0, len(tombs)):

            if (tombs[i][0] == tomb_id):

                floors = tombs[i][1]

                for j in range(0, len(floors)):

                    if (floors[j][0] == floor_id):
                         return floors[j]


    def recordScene(self, tomb_id, floor_id, floorInfo):

        #在记录时要确定当前tomb,与floor与server端是否一致，不一致判定为作弊(暂不实现)

        tombs = self.roles[0][6]

        floor = None
        tomb = None

        for i in range(0, len(tombs)):

            if (tombs[i][0] == tomb_id):

                tomb = tombs[i]

                floors = tombs[i][1]

                for j in range(0, len(floors)):

                    if (floors[j][0] == floor_id):
                        floors[j] = floorInfo
                        floor = floors[j];
                        break

        if (floor == None):

            if (tomb != None):
                tomb[1].append(floorInfo)
            else:
                tomb = TTOMB()
                tomb.extend([tomb_id, [floorInfo]])
                tombs.append(tomb)

        self.writeToDB()

    def digToTex(self,current_deep,max_deep,digTex):

        remain_deep = max_deep - current_deep

        while (current_deep > (digTex + 1) * (int)(max_deep * 0.3333)):
            digTex = digTex + 1

        return digTex

    def startDig(self, digInfo):

        tomb_id = self.roles[0][9]
        floor_id = self.roles[0][10]

        digMsg = "ok"

        tombs = self.roles[0][6]

        for i in range(0, len(tombs)):

            if (tombs[i][0] == tomb_id):

                floors = tombs[i][1]

                for j in range(0, len(floors)):

                    if (floors[j][0] == floor_id):

                        digs = floors[j][4]

                        currentDig = None

                        for k in range(0, len(digs)):
                            #如果这个dig已经存在，返回
                            if (digs[k][0] == digInfo[0]):
                                currentDig = digs[k]
                                break

                        if (currentDig == None):
                            # 根据当前层数,随机生成深度
                            minDeep = tomb_id * 20 + floor_id * 10
                            maxDeep = tomb_id * 30 + floor_id * 20
                            digInfo[4] = random.randint(minDeep, maxDeep)

                            digs.append(digInfo)

                            currentDig = digs[len(digs) - 1]


                        if(currentDig[5] >= currentDig[4]):
                            digMsg = "DIGOVER"
                        else:
                            # 开始挖掘
                            # 计算总挖掘力量
                            sumDigPower = 0;

                            if (self.roles[0][1].asDict()["stamina"] > 0):
                                sumDigPower = sumDigPower + self.roles[0][1].asDict()["digpower"]

                            for a in range(0, len(self.roles[0][4])):
                                #组队情况下，离线队员不贡献挖掘力
                                if((not self.isTeam())  or (self.roles[0][4][a].asDict()["onlinestate"]==1)):
                                    if (self.roles[0][4][a].asDict()["stamina"] > 0):
                                        sumDigPower = sumDigPower + self.roles[0][4][a].asDict()["digpower"]

                            if (sumDigPower == 0):
                                digMsg = "NOSTAMINA"
                                self.client.onDigUpdated(digInfo, TROLE(), digMsg)
                            else:
                                currentDig[5] = currentDig[5] + sumDigPower

                                currentDig[6] = min(2, self.digToTex(currentDig[5],currentDig[4],currentDig[6]))

                                #当前深度大于等于总深度
                                if(currentDig[5] >= currentDig[4]):
                                    digPosX = currentDig.asDict()["vecs"][0].asDict()["x"];
                                    digPosY = currentDig.asDict()["vecs"][0].asDict()["y"];

                                    entryX = floors[j][5][0].asDict()["vecs"][0].asDict()["x"];
                                    entryY = floors[j][5][0].asDict()["vecs"][0].asDict()["y"];

                                    entryRadius = 3

                                    if (digPosX < (entryX + entryRadius) and digPosX > (entryX - entryRadius) and
                                        digPosY < (entryY + entryRadius) and digPosY > (entryY - entryRadius)):
                                        #挖掘地点在入口半径之内
                                        currentDig[6] = 3
                                        floors[j][6] = currentDig.asDict()["vecs"][0]
                                    else:

                                        digMsg = self.itemFall(''.join([str(tomb_id),'@',str(floor_id),'@dig']))
                                        if(digMsg==''):
                                            digMsg = 'DIGNOTHING'


                                # 扣除体能
                                self.roles[0][1][0][1] = max(0, self.roles[0][1][0][1] - 3)

                                for a in range(0, len(self.roles[0][4])):
                                    self.roles[0][4][a][1] = max(0, self.roles[0][4][a][1] - 3)

                                """
                                # 值回传需要的数据
                                roleBack = TROLE()
                                roleBack[1][0][1] = self.roles[0][1][0][1]

                                for a in range(0, len(self.roles[0][4])):
                                    assist = TASSIST()
                                    assist[1] = self.roles[0][4][a][1]
                                    roleBack[4].append(assist)
                                """

                        self.client.onDigUpdated(currentDig, self.roles[0], digMsg)

                        break

        self.writeToDB()


    #根据key获取掉落列表
    def getFallListByKey(self,key):
        itemList = []
        fallList = self.gdata.fallitems.asDict()["values"]
        for i in range(0, len(fallList)):

            if(fallList[i].asDict()["key"] == key):
                itemList.append(fallList[i])

        return itemList


    #随机事件是否发生
    def randomHappen(self,probability,range):

        samples = random.randint(1, range)

        if (samples < probability):
            return True
        else:
            return False

    def itemFall (self,key):

        """
        :param key: 根据这个字段取可掉落的物品
        :return:
        """

        itemList = self.getFallListByKey(key)
        itemGet = ''

        for i in range(0, len(itemList)):

            if (self.randomHappen (itemList[i].asDict()["probability"], 101)):

                num =  random.randint(itemList[i].asDict()["minnum"], itemList[i].asDict()["maxnum"])

                if(num>0):
                    itemGet = ''.join([str(itemList[i].asDict()["itemid"]),'@',str(num),'.'])

                itemInfo = self.getItemById(itemList[i].asDict()["itemid"])

                if(itemInfo != None):
                    #加入背包(如果是雇佣兵模式，道具由玩家获得，如果是玩家最对模式，道具将roll获取)
                    #目前先实现直接放入背包

                    self.addItem(itemInfo.asDict(),num,itemInfo.asDict()["level"])

        return itemGet


	#根据item_id获取物品
    def getItemById(self,id):

        itemList = self.gdata.items.asDict()["values"]

        for i in range(0, len(itemList)):
            if(itemList[i].asDict()["dbid"] == id):
                return itemList[i]

        return None

    def playerMove(self, dir):

        #dir用于返回给队伍里的其他玩家

        #扣除体力
        self.roles[0][1][0][1] = max(0, self.roles[0][1][0][1] - 1)

        for a in range(0, len(self.roles[0][4])):
             self.roles[0][4][a][1] = max(0, self.roles[0][4][a][1] - 1)

        self.client.onPlayerMove(self.roles[0])

    #获取主场景所需数据
    def getSceneData(self,key):

        enemyTypeList = []

        typeList = self.gdata.enemytypes.asDict()["values"]

        for e in range(0, len(typeList)):
            if(typeList[e].asDict()["key"]==key):
                enemyTypeList.append(typeList[e].asDict()["enemyid"])

        self.client.OnGetSceneData(enemyTypeList)

    #获取战斗场景所需数据
    def getBattleData(self,enemyid,enemy_dbid):

        global current_enemy

        current_enemy = enemy_dbid

        iList = self.gdata.items

        #生成敌人数量
        enemy_num = random.randint(1, 3)

        enemyList = []

        for index in range(0, enemy_num):
            enemy = TBATTLE_ENEMY()
            enemy.extend([5+index, enemyid,
                          iList[enemyid].asDict()["def"],
                          iList[enemyid].asDict()["health"],
                          iList[enemyid].asDict()["health"],
                          iList[enemyid].asDict()["dodge"],
                          iList[enemyid].asDict()["attack"],
                          iList[enemyid].asDict()["price"]])
            enemyList.append(enemy)

        self.roles[0][7] = enemyList

        if(self.roles[0][8] == None):
            self.roles[0][8] = []

        self.client.OnGetBattleData(self.roles[0][7])

    def addOp(self,from_tag,to_tag,itemid):

        opList = self.roles[0][8]
        assistList = self.roles[0][4]

        op = TBATTLE_OP()
        op.extend([from_tag, to_tag, itemid])
        opList.append(op)


        self.client.onAddOp(1 if (len(self.roles[0][8])==self.getValiOpNum()) else 0)

        if(len(opList)==self.getValiOpNum()):
            #战斗开始
            self.battleStart()

    def getValiOpNum(self):
        assistList = self.roles[0][4]
        vali_op_num = 0
        if(self.roles[0][1].asDict()["health"]>0):
            vali_op_num = 1

        for i in range(0, len(assistList)):
            if(assistList[i].asDict()["health"]>0):
                vali_op_num = vali_op_num + 1

        return vali_op_num

    def battleStart(self):

        opList = self.roles[0][8]
        iList = self.gdata.items
        bggrids = self.roles[0][3]

        self.addEnemyOp()


        for i in range(0, len(opList)):

           op = opList.pop(0)

           itemid = op.asDict()["itemid"]

           if(itemid!=9000):
               fromBo = self.fromTagExplain(op.asDict()["from"])


               if(fromBo.asDict()["health"]>0):

                   if(itemid<9000):
                       for i in range(0, len(bggrids)):
                           bagInfo = bggrids[i]
                           if (bagInfo[0] == itemid):
                               itemid = bagInfo[1]
                               break

                   #通知客户端播放from动画
                   self.client.OnBattleAnim(itemid,op.asDict()["from"])

                   #留2秒给客户端播放动画
                   time.sleep(2)

                   #执行战斗命令
                   toList = self.toTagExplain(op.asDict()["to"])

                   ItemFactory.use(fromBo, toList, iList[itemid])
                   if(itemid<9000):
                       self.removeItem(iList[bagInfo[1]].asDict(), 1, op.asDict()["itemid"])

                   #通知客户端更新ui(血量 道具数量 变化)
                   self.writeToDB()

                   self.client.OnOpExe(self.formatToListChange(toList),self.roles[0][3],itemid)

                   #间隔3秒后判断是否结束战斗
                   time.sleep(3)

                   #判断战斗是否结束
                   battleRes = self.getBattleRes()
                   if(battleRes!="goon" and battleRes != "loose"):


                       tomb_id = self.roles[0][9]
                       floor_id = self.roles[0][10]

                       #移除敌人
                       floorInfo = self.getFloorInfoByTombIdFloorId(tomb_id,floor_id)

                       enemyList = floorInfo[3]

                       global current_enemy

                       for i in range(0, len(enemyList)):
                           if(enemyList[i].asDict()["dbid"]==current_enemy):
                               enemyList.remove(enemyList[i])
                               break

                       self.client.battleOver(battleRes,self.roles[0][1],self.roles[0][4],len(opList),self.roles[0][3],current_enemy)

                       current_enemy = 0

                       break
                   else:

                       playerInfoDict = {"name": "",
                              "stamina": 0,
                              "maxstamina": 0,
                              "health": 0,
                              "maxhealth": 0,
                              "strength": 0,
                              "archeology": 0,
                              "def": 0,
                              "dodge": 0,
                              "level": 0,
                              "exp": 0,
                              "digpower": 0,
                              "pro": "",
                              "img": 0,
                              "attack": 0,
                              "teamid": 0,
                              "isleader": 0,
                              "scenelevel": 0}

                       playerInfo = TPLAYER().createFromDict(playerInfoDict)

                       self.client.battleOver(battleRes,playerInfo,[],len(opList),[],0)

                       if(battleRes=="loose"):
                           break;



    #这个方法将ASSIST,PLAYER,BATTLE_ENMEY转换成同一类型，用于传输
    def formatToListChange(self,toList):

        boList = []

        for i in range(0, len(toList)):
            bo = TBATTLE_OBJ()

            dbid = 1

            if "dbid" in toList[i].asDict():
                dbid = toList[i].asDict()["dbid"]

            bo.extend([dbid, toList[i].asDict()["health"]])
            boList.append(bo)

        return boList

    #获取战斗结果
    def getBattleRes(self):
        player = self.roles[0][1]
        enemyList = self.roles[0][7]
        assistList = self.roles[0][4]

        enemyDie = True
        playerDie = True

        for i in range(0, len(enemyList)):
            if(enemyList[i].asDict()["health"]>0):
                enemyDie = False
                break

        if(player.asDict()["health"]>0):
            playerDie = False
        else:
            for i in range(0, len(assistList)):
                if(assistList[i].asDict()["health"]>0):
                    playerDie = False
                    break

        if(enemyDie):

            exp = enemyList[0].asDict()["exp"] * len(enemyList)

            #玩家获取获取经验
            playerInfoDict = self.roles[0][1].asDict()
            self.addExp(playerInfoDict, exp,self.roles[0][2], 0)
            info = TPLAYER().createFromDict(playerInfoDict)
            self.roles[0][1] = info

            #佣兵获取经验
            for i in range(0, len(assistList)):
                 assistInfoDict = assistList[i].asDict()
                 self.addExp(assistInfoDict, exp,[], assistInfoDict["iid"])
                 assist = TASSIST().createFromDict(assistInfoDict)
                 assistList[i] = assist

            #获取掉落物品
            key = ''.join([str(self.roles[0][9]),'@',str(self.roles[0][10]),'@',str(enemyList[0].asDict()["enemyid"])])

            fallMsg = self.itemFall(key)

            fallMsg = ''.join([fallMsg,'exp@',str(exp)])

            return fallMsg
        elif(playerDie):
            return "loose"
        else:
            return "goon"

    #添加敌人战斗指令
    def addEnemyOp(self):

        opList = self.roles[0][8]

        enemyList = self.roles[0][7]
        assistList = self.roles[0][4]

        #加入敌人攻击(暂时只实现普通攻击)
        #简单AI，找血最少的打
        toBo = self.roles[0][1]
        toBo_dbid = '1'
        for i in range(0, len(assistList)):
            if(assistList[i].asDict()["health"]<toBo.asDict()["health"] and assistList[i].asDict()["health"]>0):
                toBo = assistList[i]
                toBo_dbid = str(toBo.asDict()["dbid"])

        for i in range(0, len(enemyList)):

            if(enemyList[i].asDict()["health"]>0):
                op = TBATTLE_OP()
                op.extend([str(enemyList[i].asDict()["dbid"]), toBo_dbid, 9001])
                opList.append(op)


    def undoOp(self):

        opList = self.roles[0][8]
        assistList = self.roles[0][4]

        if(len(opList)>0):
            op = opList.pop(0)
            self.client.onUndoOp(op.asDict()["from"])
        else:
            self.client.onUndoOp("")

    def queryOtherPlayer(self,name,proList,page):

        playerInfos = []

        for e in KBEngine.entities.values():
            if(isinstance(e, Account)):
                if(e.databaseID != self.databaseID):

                    add_name = False
                    add_pro = False
                    add_team = True

                    info = e.roles[0][1].asDict()

                    if(name!=''):
                        if(name in info["name"]):
                            add_name = True
                    else:
                        add_name = True

                    for pro in proList:
                        if(pro==info["pro"]):
                            add_pro = True
                            break

                    if(self.roles[0][1].asDict()["teamid"]>0):
                        for ass in self.roles[0][4] :
                            if(ass.asDict()["playerid"]==e.databaseID):
                                add_team = False
                                break

                    if(add_name and add_pro and add_team):
                        e.roles[0][1][0][14] = e.databaseID #attack字段暂存数据库ID
                        playerInfos.append(e.roles[0][1])

        maxPage = int(len(playerInfos) / 5)

        if len(playerInfos)%5>0:
            maxPage=maxPage+1

        maxPage = max(1,maxPage)

        page = min(maxPage,page)
        page = max(1,page)

        playerInfosBack = []

        pageIndex = 0

        for i in range(0, 5):

            pageIndex = (page-1)*5+i

            if(pageIndex<len(playerInfos)):
                playerInfosBack.append(playerInfos[pageIndex])

        self.client.onQueryOtherPlayer(playerInfosBack,maxPage,page)

    def getAccountByDBID(self,dbid):

        account = None

        for e in KBEngine.entities.values():
            if(isinstance(e, Account)):
                if(e.databaseID == dbid):
                    account = e
                    break

        return account


    def invitePlayer(self,dbid):
        TEAM_invitePlayer(self,dbid)

    def inviteResponse(self,agreeFlag,toPlayer):
        TEAM_inviteResponse(self,agreeFlag,toPlayer)

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

        #当客户端断线的时候，如果组队了，通知队伍中的其他成员，更新自己状态为离线
        if(self.roles[0][1].asDict()["teamid"]>0):
            assistList = self.roles[0][4]

            for assist in assistList:
                playerID = assist.asDict()["playerid"]

                player = self.getAccountByDBID(playerID)

                if(player!=None):
                    player_ass = player.roles[0][4]

                    for pa in player_ass:
                        if(pa.asDict()["playerid"]==self.databaseID):
                            pa[19] = 0

                    player.client.offLineNoti(self.databaseID)


        self.destroy()

    #上线通知
    def onLineNoti(self):
        if(len(self.roles)>0):
            if(self.roles[0][1].asDict()["teamid"]>0):
                assistList = self.roles[0][4]

                for assist in assistList:
                    playerID = assist.asDict()["playerid"]

                    player = self.getAccountByDBID(playerID)

                    if(player!=None):

                        assist[19] = 1 #标识玩家在线

                        player_ass = player.roles[0][4]

                        for pa in player_ass:
                            if(pa.asDict()["playerid"]==self.databaseID):
                                pa[19] = 1 #标识玩家雇佣兵里的自己状态在线
                                break

                        player.client.onLineNoti(self.databaseID)

                    else:
                        assist[19] = 0 #将在线状态置为0

    def LeaveTeam(self,playerId,type):
        #队长统一处理，如果以后有线程安全问题，可以用同步解决
        leader = TEAM_GetLeader(self)
        leader.notifyMemberLeave(playerId,type)


    def notifyMemberLeave(self,playerId,type):

        leavePlayerAccount = None

        #如果是队长离队，将队长职位转交
        if(self.databaseID == playerId):
            self.giveLeader(0)
            leavePlayerAccount = self
        else:
            leavePlayerAccount =  self.getAccountByDBID(playerId)

        if(leavePlayerAccount!=None):
            for ass in leavePlayerAccount.roles[0][4] :
                 assId = ass.asDict()["playerid"]
                 assAccount = self.getAccountByDBID(assId)

                 if(assAccount != None):
                     for ass_ass in assAccount.roles[0][4]:
                         if(ass_ass.asDict()["playerid"] == playerId):
                             assAccount.roles[0][4].remove(ass_ass)
                             break

                     assAccount.writeToDB()
                     assAccount.client.PlayerLeave(playerId,type)

            leavePlayerAccount.roles[0][4] = []
            leavePlayerAccount.roles[0][1][0][15] = 0
            leavePlayerAccount.writeToDB()
            leavePlayerAccount.client.PlayerLeave(playerId,type)


    def RecordSceneLevel(self,level):
        self.roles[0][1][0][17] = level

    def giveLeader(self,playerId):
        if(playerId == 0):
            #自动转交，掉线或者离队
            self.roles[0][1][0][16] = 0
            playerId = self.roles[0][4][0].asDict()["playerid"]

        playerAccount = self.getAccountByDBID(playerId)
        playerAccount.roles[0][1][0][16] = 1
        #更新队伍ID
        playerAccount.roles[0][1][0][15] = playerId
        playerAccount.client.LeaderChange(1)
        self.client.LeaderChange(0)

        #更新队伍ID
        for ass in playerAccount.roles[0][4] :
            assAccount = self.getAccountByDBID(assId)
            if(assAccount!=None):
                assAccount.roles[0][1][0][15] = playerId

    def DoTeam(self, invitePlayer):

        selfAD = PlayerDataToAssist(self.roles[0][1].asDict(),self.databaseID)
        invitePlayerAD = PlayerDataToAssist(invitePlayer.roles[0][1].asDict(),invitePlayer.databaseID)

        #设置队伍ID
        if(self.roles[0][1].asDict()["teamid"]==0):
            self.roles[0][1][0][15] = self.databaseID  #队长id作为队伍id
            self.roles[0][1][0][16] = 1 #队长标志

        invitePlayer.roles[0][1][0][15] = self.databaseID

        #添加到雇佣兵列表
        #1.添加队长
        invitePlayer.roles[0][4].append(selfAD);
        #2.添加队长雇佣兵，也就是其他玩家
        leaderAssList = self.roles[0][4]

        for ass in leaderAssList:
            invitePlayer.roles[0][4].append(ass);
            assId = ass.asDict()["playerid"]
            #通知其他队员添加这个玩家
            otherMember = self.getAccountByDBID(assId)
            otherMember.roles[0][4].append(invitePlayerAD);
            otherMember.writeToDB()
            otherMember.client.onInvitePlayer("ok", otherMember.roles[0][4],0)

        #3.队长添加这个玩家
        self.roles[0][4].append(invitePlayerAD);
        self.client.onInvitePlayer("ok", self.roles[0][4],1)

        invitePlayer.writeToDB()
        invitePlayer.client.onInvitePlayer("ok", invitePlayer.roles[0][4],2)

    def isTeam(self):
        if(self.roles[0][1].asDict()["teamid"]>0):
            return True
        else:
            return False