from KBEDebug import *


class ItemFactory:

    @staticmethod
    def use(fromBo,toList,itemInfo):

        itemid = itemInfo.asDict()["dbid"];

        if(itemid != 9000): #等待操作不计算
            for i in range(0, len(toList)):

                toBo = ItemFactory.typeConvertor(toList[i])

                if(itemid==9001): #普通攻击
                    attack = fromBo.asDict()["attack"]
                    defend = toList[i].asDict()["def"]
                    toBo[3] = max(toBo[3] - max(0,(attack - defend)),0)

                elif(itemInfo.asDict()["commontype"]==3):
                    heal = itemInfo.asDict()["health"]
                    toBo[3] = min(toBo[3] + heal,toBo[4])


    @staticmethod
    def typeConvertor(old_one):
        if(isinstance(old_one, dict)):
            return old_one[0]
        else:
            return old_one




