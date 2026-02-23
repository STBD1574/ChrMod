# -*- encoding: utf-8 -*-
class ListenLibraryNode(object):
    def __init__(self, listener):
        self.listener = listener
        self.library = []


class ListenLibrary(object):
    def __init__(self):
        # nodes
        self.library = []
        self.proxy_library = []

    def AddListener(self, listener):
        for node in self.library:
            if node.listener == listener:
                return False

        new_node = ListenLibraryNode(listener)
        self.library.append(new_node)

    def AddEvent(self, listener, eventName, callbackFunction):
        for node in self.library:
            if node.listener == listener:
                node.library.append((eventName, callbackFunction))
                return True
        return False

    def AddListenerProxy(self, listener_proxy):
        for proxy in self.library:
            if proxy == listener_proxy:
                return False

        self.proxy_library.append(listener_proxy)


class ListenerFactory(object):
    def __init__(self):
        self.library = ListenLibrary()

    def CreateListener(self, systemName, namespace):
        listener = Listener(self, systemName, namespace)
        self.library.AddListener(listener)
        return listener

    def AddEvent(self, listener, eventName, callbackFunction):
        return self.library.AddEvent(listener, eventName, callbackFunction)

    def CreateListenerProxy(self):
        listener_proxy = ListenerProxy(self)
        self.library.AddListenerProxy(listener_proxy)
        return listener_proxy

    def ShowAll(self):
        print("-----------------------------------")
        print("Factory:", self)
        print("ListenLibrary:", self.library)
        print("proxys:", self.library.proxy_library)
        print("-----------------------------------")
        for node in self.library.library:
            print("-----------------------------------")
            print("listener:", node.listener)
            for data in node.library:
                print("datas:", data[0], data[1])
            print("-----------------------------------")

    def DeleteAll(self):
        for node in self.library.library:
            del node.listener
            for data in node.library:
                del data[0]
                del data[1]
            del node.library
        del self.library.library

        for proxy in self.library.proxy_library:
            del proxy

        del self.library.proxy_library

        del self.library
        del self


class Listener(object):
    def __init__(self, factory, systemName, namespace):
        self.factory = factory
        self.systemName = systemName
        self.namespace = namespace

    def __call__(self, eventName):
        def decorator(decorated_function):
            self.AddEvent(eventName, decorated_function)
            return decorated_function
        return decorator

    def AddEvent(self, eventName, callbackFunction):
        return self.factory.AddEvent(self, eventName, callbackFunction)


class ListenerProxy(object):
    def __init__(self, factory):
        self.factory = factory

    def __call__(self):
        def decorator(decorated_class):
            proxy = self
            class ProxyClass(decorated_class):
                def __init__(self, *args, **kwargs):
                    decorated_class.__init__(self, *args, **kwargs)
                    for node in proxy.factory.library.library:
                        listener = node.listener
                        systemName = listener.systemName
                        namespace = listener.namespace
                        for data in node.library:
                            self.ListenForEvent(namespace, systemName, data[0], self, data[1])
            return ProxyClass
        return decorator
