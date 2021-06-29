__all__ = [
    "TaskQueue",
    "MaxRetryError",
]

import logging
import queue

from .thread_manager import ThreadManager

logger = logging.getLogger(__name__)


class MaxRetryError(RuntimeError):
    pass


class TaskQueue:
    def __get_tid(self) -> int:
        tid = self.__max_tid
        self.__max_tid += 1
        return tid

    def __worker(self):
        while self.__running:
            try:
                queue_data = self.__task_queue.get(timeout=0.25)
                tid = queue_data["tid"]
                args = queue_data["args"]
                retry = queue_data["retry"]
                callback = queue_data["callback"]
                retry_times = queue_data["retry_times"]
                max_retry_times = queue_data["max_retry_times"]
                try:
                    if retry_times >= max_retry_times:
                        raise MaxRetryError(f"Max retry times: {max_retry_times}, now retry times: {retry_times}")
                    data = self.__worker_func(*args)
                    if callback is not None:
                        callback_return = callback(data)
                    else:
                        callback_return = None
                    self.__tid_return_map[tid] = {
                        "err": False,
                        "data": data,
                        "callback_return": callback_return,
                    }

                except MaxRetryError as err:
                    self.__tid_return_map[tid] = {
                        "err": True,
                        "data": err,
                        "history_errs": self.__tid_history_err_map.pop(tid),
                    }

                except Exception as err:
                    if retry:
                        self.__tid_history_err_map.setdefault(tid, []).append(err)
                        self.add_task(*args,
                                      tid=tid,
                                      retry=retry,
                                      callback=callback,
                                      retry_times=retry_times + 1,
                                      max_retry_times=max_retry_times,
                                      )
                    else:
                        self.__tid_return_map[tid] = {
                            "err": True,
                            "data": err,
                        }
            except queue.Empty:
                pass

    def __init__(self, func, pool_size=1):
        if pool_size <= 0:
            raise RuntimeError(f"Pool size must > 0: {pool_size}")
        self.__running = True
        self.__max_tid = 0
        self.__task_queue = queue.Queue()
        self.__tm = ThreadManager()
        self.__worker_func = func
        self.__tid_return_map = {}
        self.__tid_history_err_map = {}
        for _ in range(pool_size):
            self.__tm.apply(self.__worker)

    def add_task(self,
                 *args,
                 tid=None,
                 retry=False,
                 callback=None,
                 retry_times=0,
                 max_retry_times=3) -> int:
        if tid is None:
            tid = self.__get_tid()

        self.__task_queue.put({
            "tid": tid,
            "args": args,
            "retry": retry,
            "retry_times": retry_times,
            "max_retry_times": max_retry_times,
            "callback": callback,
        })
        return tid

    def stop(self):
        self.__running = False
        self.__tm.join()

    def pop_return_by_tid(self, tid):
        return self.__tid_return_map.pop(tid, None)


if __name__ == '__main__':
    import time


    def start_tq(func):
        tq = TaskQueue(func, pool_size=10)
        tid_list = []
        for i in range(3):
            tid_list.append(tq.add_task(i, retry=True, callback=echo))

        time.sleep(3)
        tq.stop()

        for tid in tid_list:
            print(tid, tq.pop_return_by_tid(tid))


    def echo(x):
        return x


    def test_err(_):
        raise RuntimeError("Error")


    start_tq(echo)
    start_tq(test_err)
