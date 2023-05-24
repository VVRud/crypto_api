from threading import Thread

from modules.singleton import Singleton


class SingletonClass(Singleton):
    def __init__(self, value):
        self.value = value


class CustomThread(Thread):
    # constructor
    def __init__(self, value):
        Thread.__init__(self)
        self.singleton_value = value
        self.singleton = None

    def run(self):
        self.singleton = SingletonClass(self.singleton_value)


def test_singleton_single_thread():
    s1 = SingletonClass(0)
    s2 = SingletonClass(1)

    assert s1.value == s2.value
    assert s1 is s2


def test_singleton_multi_thread():
    process1 = CustomThread(value=0)
    process2 = CustomThread(value=1)
    process1.start()
    process2.start()
    process1.join()
    process2.join()

    assert process1.singleton.value == process2.singleton.value
    assert process1.singleton is process2.singleton
