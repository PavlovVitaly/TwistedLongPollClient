from twisted.internet import reactor, protocol
import pickle


class GetterLongPollConnect(protocol.Protocol):

    def connectionMade(self):
        result_dict = dict()
        result_dict['login'] = 'user'
        result_dict['password'] = 'pass'
        self.transport.write(pickle.dumps(result_dict))

    def dataReceived(self, data):
        get_request = pickle.loads(data)
        print("Server said:", get_request)
        if get_request[0] == 'get':
            port = get_request[1].get('server')
            port = port.split(':')
            port = port[2]
            reactor.connectTCP("localhost", int(port), LongPollConnectionFactory(get_request[1].get('key'), get_request[1].get('ts')))
        self.transport.loseConnection()


class GetterLongPollConnectFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return GetterLongPollConnect()

    def clientConnectionFailed(self, connector, reason):
        print("Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("Connection lost.")
        # reactor.stop()


class LongPollConnection(protocol.Protocol):
    def __init__(self, long_poll_get):
        self.__long_poll_get = long_poll_get

    def connectionMade(self):
        req = pickle.dumps(self.__long_poll_get)
        self.transport.write(req)

    def dataReceived(self, data):
        get_request = pickle.loads(data)
        print("Server said:", get_request)
        self.transport.loseConnection()


class LongPollConnectionFactory(protocol.ClientFactory):
    def __init__(self, key, ts):
        self.__long_poll_get = {'key': key, 'ts': ts}

    def buildProtocol(self, addr):
        return LongPollConnection(self.__long_poll_get)


reactor.connectTCP("localhost", 8000, GetterLongPollConnectFactory())
reactor.connectTCP("localhost", 8000, GetterLongPollConnectFactory())
reactor.connectTCP("localhost", 8000, GetterLongPollConnectFactory())
reactor.run()
