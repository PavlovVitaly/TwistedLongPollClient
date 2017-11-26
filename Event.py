from datetime import datetime


class Event(object):
    def __init__(self, description_of_event):
        self.__timestamp = datetime.now()
        self.__description_of_event = description_of_event

    @property
    def timestamp(self):
        return self.__timestamp

    @property
    def description_of_event(self):
        return self.__description_of_event

    def __lt__(self, other):
        return self.__timestamp < other.__timestamp

    def __le__(self, other):
        return self.__timestamp <= other.__timestamp

    def __eq__(self, other):
        return self.__timestamp == other.__timestamp

    def __ne__(self, other):
        return self.__timestamp != other.__timestamp

    def __gt__(self, other):
        return self.__timestamp > other.__timestamp

    def __ge__(self, other):
        return self.__timestamp >= other.__timestamp


if __name__ == '__main__':
    a = Event('a')
    b = Event('b')
    print(a <= b)
