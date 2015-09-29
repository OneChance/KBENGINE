# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ASSIST import *

def TEAM_invitePlayer(account, dbid):
    # 判断当前玩家的队伍信息
    if (account.roles[0][1].asDict()["teamid"] > 0):
        if (account.roles[0][1].asDict()["isleader"] == 0):
            account.client.onInvitePlayer("NEEDBELEADER", [])
            return

        if (len(account.roles[0][4])==3):
            account.client.onInvitePlayer("TEAMFULL", [])
            return


    # 判断当前是否有雇佣兵
    check_msg = check_assist(account)

    if (check_msg != "ok"):
        account.client.onInvitePlayer(check_msg, [])
        return

    invite_player = account.getAccountByDBID(dbid)

    if (invite_player != None):
        # 检测这个玩家是否已经组队
        invite_player_assistList = invite_player.roles[0].asDict()["assists"]

        onlineTeam = False

        for assist in invite_player_assistList:
            if (assist.asDict()["player"] == 1):
                onlineTeam = True
                break

        if (onlineTeam):
            account.client.onInvitePlayer("PLAYERTEAMED", [])
            return

        # 向玩家发送邀请
        account.roles[0][1][0][14] = account.databaseID
        invite_player.client.onInvited(account.roles[0][1])
    else:
        account.client.onInvitePlayer("NOPLAYER", [])


def check_assist(account):
    msg = "ok"
    assistList = account.roles[0].asDict()["assists"]

    for assist in assistList:
        if (assist.asDict()["player"] == 0):
            msg = "PLEASEREMOVEASSIST"
            break

    return msg


def TEAM_inviteResponse(account, agreeFlag, toPlayer):
    invite_player = account.getAccountByDBID(toPlayer)

    if (invite_player != None):
        if (agreeFlag == 1):
            # 判断当前是否有雇佣兵
            check_msg = check_assist(account)

            if (check_msg != "ok"):
                account.client.onInvitePlayer("PLAYERTEAMED", [])
                invite_player.client.onInvitePlayer(check_msg, [])
                return

            # 执行组队逻辑
            DoTeam(account, invite_player)

            #调用各自客户端，更新雇佣兵列表
            account.client.onInvitePlayer("ok", account.roles[0][4])
            invite_player.client.onInvitePlayer("ok", invite_player.roles[0][4])

        else:
            invite_player.client.onInvitePlayer("INVITEREJECT", [PlayerDataToAssist(account.roles[0][1].asDict(),account.databaseID)])
    else:
        account.client.onInvitePlayer("NOPLAYER", [])


def DoTeam(account, invite_player):
    """
    @account		: 当前应答玩家
    @invite_player	: 发出邀请的玩家
    """
    account_a = PlayerDataToAssist(account.roles[0][1].asDict(),account.databaseID)
    invite_player_a = PlayerDataToAssist(invite_player.roles[0][1].asDict(),invite_player.databaseID)

    #设置队伍ID
    if(invite_player.roles[0][1].asDict()["teamid"]==0):
        invite_player.roles[0][1][0][15] = invite_player.databaseID #队长id作为队伍id
        invite_player.roles[0][1][0][16] = 1 #队长标志
    account.roles[0][1][0][15] = invite_player.databaseID

    ERROR_MSG("do team")

    #相互添加到雇佣兵列表
    account.roles[0][4].append(invite_player_a);
    invite_player.roles[0][4].append(account_a);


def PlayerDataToAssist(playerData,dbid):
    assistData = TASSIST()

    assistData.extend(
        [0, playerData["stamina"],
         playerData["maxstamina"],
         playerData["health"],
         playerData["maxhealth"],
         playerData["img"],
         playerData["level"],
         0,
         playerData["strength"],
         playerData["archeology"],
         playerData["def"],
         playerData["dodge"],
         playerData["exp"],
         playerData["digpower"],
         playerData["attack"], 1, playerData["name"],playerData["pro"], dbid,1])

    return assistData;

