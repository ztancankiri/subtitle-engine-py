class Node:
    def __init__(self, task, param):
        self.task = task
        self.param = param
        self.positive = None
        self.negative = None

    def setNexts(self, positive, negative):
        self.positive = positive
        self.negative = negative

    def isFinal(self):
        return self.positive == None and self.negative == None

    def run(self):
        result = self.task(self.param)

        if (not self.isFinal()):
            if (result == True):
                self.positive.run()
            elif (result == False):
                self.negative.run()
