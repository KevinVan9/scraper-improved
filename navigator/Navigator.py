from abc import ABC, abstractmethod
class Navigator:

    driver = None
    LINK = None

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def nextPage(self):
        pass

    @abstractmethod
    def prevPage(self):
        pass

    @abstractmethod
    def nextItem(self):
        pass

    @abstractmethod
    def extractItem(self):
        pass
