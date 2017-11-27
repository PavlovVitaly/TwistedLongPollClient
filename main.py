from twisted.internet import reactor, protocol
import pickle
from Event import Event


class GetterLongPollConnect(protocol.Protocol):
    def __init__(self):
        self.menu_dict = {'1': self.client_login, '2': self.client_register, '3': self.exit}

    def connectionMade(self):
        request = self.show_menu()
        self.transport.write(pickle.dumps(request))

    def dataReceived(self, data):
        get_request = pickle.loads(data)
        print("Server said:", get_request)
        if get_request[0] == 'get':
            port = get_request[1].get('server')
            port = port.split(':')
            port = port[2]
            reactor.connectTCP("localhost", int(port), LongPollConnectionFactory(get_request[1].get('key'), get_request[1].get('ts')))
        elif get_request[0] == 'successful_registration':
            print(get_request[0])
        self.transport.loseConnection()

    def client_login(self):
        request = list()
        request.append('login')
        result_dict = dict()
        result_dict['login'] = input("Введите Ваш login:")
        result_dict['password'] = input("Ведите пароль:")
        request.append(result_dict)
        return request

    def client_register(self):
        request = list()
        request.append('register')
        result_dict = dict()
        result_dict['login'] = input("Введите Ваш login:")
        result_dict['password'] = input("Ведите пароль:")
        request.append(result_dict)
        return request

    def exit(self):
        self.connectionLost('')
        reactor.stop()

    def show_menu(self):
        result = None
        while not result:
            choice = input("Выберите дальнейшее действие:\n1. Войти в систему.\n2. Зарегистрироваться\n3. Выйти\n")
            show_point = self.menu_dict.get(choice)
            if show_point is None:
                print('Ошибка ввода! Повторите ввод.\n')
                continue
            result = show_point()
        return result


class GetterLongPollConnectFactory(protocol.ClientFactory):

    def buildProtocol(self, addr):
        return GetterLongPollConnect()

    def clientConnectionFailed(self, connector, reason):
        print("GET: Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("GET: Connection lost.")
        # reactor.stop()


class LongPollConnection(protocol.Protocol):
    def __init__(self, long_poll_get):
        self.__long_poll_get = long_poll_get

    def connectionMade(self):
        print('LONG POLL: Connection is made.')
        req = pickle.dumps(self.__long_poll_get)
        self.transport.write(req)

    def dataReceived(self, data):
        get_request = pickle.loads(data)
        if get_request[0] == 'event':
            print("Server said:")
            print('ts: ', get_request[1].timestamp)
            print('description: ', get_request[1].description_of_event)
            print('')
        elif get_request[0] == 'cashed_events':
            print("Server said:")
            for event in get_request[1]:
                print("Server said:")
                print('ts: ', event.timestamp)
                print('description: ', event.description_of_event)
                print('')

    def clientConnectionFailed(self, connector, reason):
        print("LONG POLL: Connection failed.")
        reactor.stop()

    def clientConnectionLost(self, connector, reason):
        print("LONG POLL: Connection lost.")
        # reactor.stop()


class LongPollConnectionFactory(protocol.ClientFactory):
    def __init__(self, key, ts):
        self.__long_poll_get = {'key': key, 'ts': ts}

    def buildProtocol(self, addr):
        return LongPollConnection(self.__long_poll_get)


reactor.connectTCP("localhost", 8000, GetterLongPollConnectFactory())
reactor.run()
