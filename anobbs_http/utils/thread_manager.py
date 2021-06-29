__all__ = [
    "ThreadManager",
]

from threading import Thread


class ThreadManager:
    def __init__(self):
        self.__thread_list = []

    def apply(self, func, *args, **kwargs):
        t = Thread(target=func, args=args, kwargs=kwargs)
        self.__thread_list.append(t)
        t.start()

    def join(self):
        for t in self.__thread_list:
            t.join()
        self.__thread_list = []
