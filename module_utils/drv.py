# -*- coding: utf-8 -*-
# @Author: ronanjs
# @Date:   2020-01-19 22:23:54
# @Last Modified by:   ronanjs
# @Last Modified time: 2020-07-02 10:52:19


class DRV:

    def __init__(self, objects, rest):
        self.objects = objects
        self.rest = rest

    def subscribe(self):

        drvHandles = self.objects.handles()
        self.rest.perform(
            "SubscribeDynamicResultView", {"DynamicResultView": " ".join(drvHandles)}
        )
        return None

    def fetch(self):

        drvHandles = self.objects.handles()

        self.rest.perform(
            "UpdateDynamicResultViewCommand", {"DynamicResultView": " ".join(drvHandles)}
        )

        data = []
        for handle in drvHandles:

            prqHandle = self.rest.get(handle, ["children-PresentationResultQuery"])

            columns = self.rest.get(prqHandle,["SelectProperties"]).split(" ")
            resHandles = self.rest.get(prqHandle, ["children-ResultViewData"])

            if resHandles == "":
                # print("There are no result for ...",handle)
                continue

            for handle in resHandles.split(" "):
                resdata = self.rest.get(handle,["ResultData"])
                values = stcStringSplit(resdata)
                row = {}
                for i in range(len(columns)):
                    row[columns[i]]=values[i]
                data.append(row)

        return data



def stcStringSplit(s):
    cols = []
    concat = ""
    for term in s.split(" "):
        if term[0] == "{":
            concat = term[1:]
        elif term[-1] == "}":
            cols.append(concat + " " + term[:-1])
            concat = ""
        elif len(concat) > 0:
            concat + " " + term
        else:
            cols.append(term)
    return cols


