class Person():
    def __init__(self,head,body,leg):
        self.head = head
        self.body = body
        self.leg = leg
        self.baby = 0
    def calculcate_length(self):
        length = self.head + self.body + self.leg
        return length

    def calculcate_weight(self):
        weight = (self.head + self.body + self.leg)*100
        return weight

    @property
    def baby(self):
        return self.__baby

    @baby.setter
    def baby(self,baby):
        self.__baby = baby

