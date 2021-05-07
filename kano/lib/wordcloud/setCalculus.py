class setCalc:
    def __init__(self, d1, d2):
        self.dict1_num = d1
        self.dict2_num = d2
        self.dict1 = dict(d1)
        self.dict2 = dict(d2)

        sum1 = 0
        for d in self.dict1:
            sum1+=self.dict1[d]

        maxVal1=max(self.dict1.values())
        for d in self.dict1:
            #self.dict1[d] /= sum1
            self.dict1[d] /= maxVal1

        sum2 = 0
        for d in self.dict2:
            sum2+=self.dict2[d]

        maxVal2=max(self.dict2.values())
        for d in self.dict2:
            #self.dict2[d] /= sum2
            self.dict2[d] /= maxVal2

    def getInter_keyword_num(self):
        samekeys = self.dict1_num.keys() & self.dict2_num.keys()
        intersect = {}
        for k in samekeys:
            v = min(self.dict1_num[k], self.dict2_num[k])
            intersect[k] = v
        return intersect

    def getDiff1_keyword_num(self):
        inter = self.getInter_keyword_num()
        diffa = dict(self.dict1_num)
        for i in inter:
            diffa[i] = self.dict1_num[i] - inter[i]
        return diffa

    def getDiff2_keyword_num(self):
        inter = self.getInter_keyword_num()
        diffb = dict(self.dict2_num)
        for i in inter:
            diffb[i] = self.dict2_num[i] - inter[i]
        return diffb

    def getInter(self):
        samekeys = self.dict1.keys()&self.dict2.keys()
        intersect = {}
        for k in samekeys:
            v = min(self.dict1[k],self.dict2[k])
            intersect[k]=v
        return intersect

    # def getDiff1(self):
    #     inter = self.getInter()
    #     diffa = dict(self.dict1)
    #     for i in inter:
    #         diffa[i] = self.dict1[i] - inter[i] - self.dict2[i]
    #     basea = abs(min(diffa.values()))
    #     for i in diffa:
    #         diffa[i] += basea
    #     return diffa

    def getDiff1(self):
        inter=self.getInter()
        diffa = dict(self.dict1)
        for i in inter:
            diffa[i]=self.dict1[i]-inter[i]
        return diffa

    # def getDiff2(self):
    #     inter = self.getInter()
    #     diffb = dict(self.dict2)
    #     for i in inter:
    #         diffb[i] = self.dict2[i] - inter[i] - self.dict1[i]
    #     baseb = abs(min(diffb.values()))
    #     for i in diffb:
    #         diffb[i] += baseb
    #     return diffb
    def getDiff2(self):
        inter=self.getInter()
        diffb = dict(self.dict2)
        for i in inter:
            diffb[i]=self.dict2[i]-inter[i]
        return diffb


class setCalckey3:
    def __init__(self, d1, d2, d3):
        self.dict1 = dict(d1)
        self.dict2 = dict(d2)
        self.dict3 = dict(d3)

        sum1 = 0
        for d in self.dict1:
            sum1 += self.dict1[d]

        maxVal1 = max(self.dict1.values())
        for d in self.dict1:
            # self.dict1[d] /= sum1
            self.dict1[d] /= maxVal1

        sum2 = 0
        for d in self.dict2:
            sum2 += self.dict2[d]

        maxVal2 = max(self.dict2.values())
        for d in self.dict2:
            # self.dict2[d] /= sum2
            self.dict2[d] /= maxVal2

        sum3 = 0
        for d in self.dict3:
            sum3 += self.dict3[d]

        maxVal3 = max(self.dict3.values())
        for d in self.dict3:
            # self.dict3[d] /= sum3
            self.dict3[d] /= maxVal3

    def getInterG(self):
        samekeys = self.dict1.keys() & self.dict2.keys() & self.dict3.keys()
        intersectg = {}
        for k in samekeys:
            v = min(self.dict1[k], self.dict2[k], self.dict3[k])
            intersectg[k] = v
        return intersectg

    def getInterD(self):
        interg = self.getInterG()
        samekeysAB = self.dict1.keys() & self.dict2.keys()
        intersectab = {}
        for k in samekeysAB:
            v = min(self.dict1[k], self.dict2[k])
            intersectab[k] = v
        intersectd = dict(intersectab)
        for i in interg:
            intersectd[i] -= interg[i]
        return intersectd

    def getInterE(self):
        interg = self.getInterG()
        samekeysAC = self.dict1.keys() & self.dict3.keys()
        intersectac = {}
        for k in samekeysAC:
            v = min(self.dict1[k], self.dict3[k])
            intersectac[k] = v
        intersecte = dict(intersectac)
        for i in interg:
            intersecte[i] -= interg[i]
        return intersecte

    def getInterF(self):
        interg = self.getInterG()
        samekeysBC = self.dict2.keys() & self.dict3.keys()
        intersectbc = {}
        for k in samekeysBC:
            v = min(self.dict2[k], self.dict3[k])
            intersectbc[k] = v
        intersectf = dict(intersectbc)
        for i in interg:
            intersectf[i] -= interg[i]
        return intersectf

    def getDiffA(self):
        interD = self.getInterD()
        interE = self.getInterE()
        interG = self.getInterG()
        interDEG = {**interD, **interE, **interG}
        diffa = dict(self.dict1)
        for i in interDEG:
            diffa[i] -= interDEG[i]
        return diffa

    def getDiffB(self):
        interD = self.getInterD()
        interF = self.getInterF()
        interG = self.getInterG()
        interDFG = {**interD, **interF, **interG}
        diffb = dict(self.dict2)
        for i in interDFG:
            diffb[i] -= interDFG[i]
        return diffb

    def getDiffC(self):
        interE = self.getInterE()
        interF = self.getInterF()
        interG = self.getInterG()
        interEFG = {**interE, **interF, **interG}
        diffc = dict(self.dict3)
        for i in interEFG:
            diffc[i] -= interEFG[i]
        return diffc


