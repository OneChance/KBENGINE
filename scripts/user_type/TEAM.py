# -*- coding: utf-8 -*-
import KBEngine
from KBEDebug import *
from ASSIST import *

def TEAM_invitePlayer(account, dbid):
    # 判断当前玩家的队伍信息
    if (account.roles[0][1].asDict()["teamid"] > 0):
        if (account.roles[0][1].asDict()["isleader"] == 0):
            account.client.onInvitePlayer("NEEDBELEADER", [],0)
            return

        if (len(account.roles[0][4])==3):
            account.client.onInvitePlayer("TEAMFULL", [],0)
            return


    # 判断当前是否有雇佣兵
    check_msg = check_assist(account)

    if (check_msg != "ok"):
        account.client.onInvitePlayer(check_msg, [],0)
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
            account.client.onInvitePlayer("PLAYERTEAMED", [],0)
            return

        if (invite_player.roles[0][1].asDict()["scenelevel"] > 2):
            account.client.onInvitePlayer("PLAYEROUT", [],0)
            return

        # 向玩家发送邀请
        account.roles[0][1][0][14] = account.databaseID
        invite_player.client.onInvited(account.roles[0][1])
    else:
        account.client.onInvitePlayer("NOPLAYER", [],0)


def check_assist(account):
    msg = "ok"
    assistList = account.roles[0].asDict()["assists"]

    for assist in assistList:
        if (assist.asDict()["player"] == 0):
            msg = "PLEASEREMOVEASSIST"
            break

    return msg


def TEAM_inviteResponse(account, agreeFlag, toPlayer):

    """
    :param account:
    :param agreeFlag:
    :param toPlayer:  要应答的玩家，即队长
    :return:
    """

    invite_player = account.getAccountByDBID(toPlayer)

    if (invite_player != None):
        if (agreeFlag == 1):
            # 判断当前是否有雇佣兵
            check_msg = check_assist(account)

            if (check_msg != "ok"):
                account.client.onInvitePlayer("PLAYERTEAMED", [],0)
                invite_player.client.onInvitePlayer(check_msg, [],0)
                return

            # 执行组队逻辑
            invite_player.DoTeam(account)

        else:
            invite_player.client.onInvitePlayer("INVITEREJECT", [PlayerDataToAssist(account.roles[0][1].asDict(),account.databaseID)],0)
    else:
        account.client.onInvitePlayer("NOPLAYER", [],0)



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

def TEAM_GetLeader(account):

    if(account.roles[0][1].asDict()["isleader"] == 1):
        return account
    else:
        for member in account.roles[0][4] :
            memberAccount = account.getAccountByDBID(member.asDict()["playerid"])
            if(memberAccount.roles[0][1].asDict()["isleader"] == 1):
                return memberAccount

    return None