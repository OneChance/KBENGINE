from KBEDebug import *


class ItemFactory:

    def use(fromTag,toList,itemInfo):
        for i in range(0, len(toList)):
            if(itemInfo.asDict()["commontype"]==3):
                heal = itemInfo.asDict()["health"]

                ERROR_MSG("heal=%r" % (heal));

                toList[i][3] = min(toList[i][3] + heal,toList[i][4])
                ERROR_MSG("health=%r" % (toList[i][3]));



