import threading
import collections
import queue


class Threadium:
    def __init__(self, tk):
        """
        - tk: a tk.Tk instance
        """
        self._tk = tk
        self._internal_count = 0
        self._queues = dict()
        self._queues_lock = threading.Lock()
        self._executing_sync_task_lock = threading.Lock()
        self._waiting_sync_tasks = list()
        self._executing_sync_task = False


    # ===========================================
    #               PUBLIC METHODS
    # ===========================================
    def q(self):
        """
        Creates a new Queue
        """
        return queue.Queue()

    def consume(self, queue, consumer=None, unpack_result=False,
                exception_handler=None, latency=10):
        """
        Loops through the queue, pick data, then run the callback 'consumer' with
        data as argument.
        Example, assume that there are these integers 3, 4 and 5 in the queue.
        3 -> consumer(3); 4 -> consumer(4); 5 -> consumer(5)

        - queue: the queue. See Threadium's method 'q'.
        - consumer: the callback that accepts one argument or more than one if unpack_result is True
        - unpack_result: if True, the result will be unpacked.
        - exception_handler: callback that accepts one argument to handle any occurred exception.
        - latency: integer. Milliseconds between each loop to consume the queue. By default: 10

        Returns the 'qid'. You will need this 'qid' to stop, pause, resume the loop or to get info.
        """
        qid = self._consume(queue,
                            consumer,
                            unpack_result,
                            exception_handler,
                            latency)
        return qid

    def pause(self, qid):
        """
        Pause the process launched by the method 'consume'.
        Put 0 to pause all processes
        """
        if qid == 0:
            with self._queues_lock:
                for key in self._queues.keys():
                    self._queues[key]["active"] = False
        elif self._is_valid_qid(qid):
            with self._queues_lock:
                self._queues[qid]["active"] = False

    def resume(self, qid):
        """
        Resume the process launched by the method 'consume'
        Put 0 to resume all processes
        """
        if qid == 0:
            with self._queues_lock:
                for key in self._queues.keys():
                    if not self._queues[key]["active"]:
                        self._queues[key]["active"] = True
                        self._loop(key)
        elif self._is_valid_qid(qid):
            with self._queues_lock:
                if not self._queues[qid]["active"]:
                    self._queues[qid]["active"] = True
                    self._loop(qid)

    def stop(self, qid):
        """
        Stop the process launched by the method 'consume'.
        Set 0 to stop them all.
        """
        if qid == 0:
            with self._queues_lock:
                self._queues = dict()
        elif self._is_valid_qid(qid):
            with self._queues_lock:
                del self._queues[qid]

    def info(self, qid):
        """
        Retrieve info from the process launched by the method 'consume'.
        Returns a dict:
         {"queue": queue, "active": boolean, "consumer": callback, "unpack_result": boolean,
         "exception_handler": callback, "latency": integer}
        """
        if not self._is_valid_qid(qid):
            return
        if qid == 0:
            return tuple([x.copy() for x in self._queues])
        return self._queues[qid].copy()

    def task(self, host, args=[], kwargs={},
             consumer=None,
             sync=False,
             unpack_result=False,
             upstream_exception_handler=None,
             downstream_exception_handler=None):
        """
        Executes a task in background. Return False if the task is WAITING (sync)
        - host: the host to call
        - args: arguments to use
        - kwargs: keyword-arguments to use
        - consumer: the callback with parameter(s) that will consume the returned value by host
        - sync
        - unpack_result: boolean, True, to unpack the result returned by host
        - upstream_exception_handler: one parameter callback to handle the exception
            raised while running the host
        - downstream_exception_handler: one parameter callback to handle the exception
            raised while calling the consumer
        """
        return self._task(host, args, kwargs, consumer,
                          sync,
                          unpack_result,
                          upstream_exception_handler,
                          downstream_exception_handler)

    # ===========================================
    #               INTERNAL
    # ===========================================
    def _task(self, host, args, kwargs, consumer,
              sync,
              unpack_result,
              upstream_exception_handler,
              downstream_exception_handler):
        with self._executing_sync_task_lock:
            if sync and self._executing_sync_task:
                data = {"host": host, "args": args, "kwargs": kwargs,
                        "consumer": consumer, "sync": sync,
                        "unpack_result": unpack_result,
                        "upstream_exception_handler": upstream_exception_handler,
                        "downstream_exception_handler": downstream_exception_handler}
                self._waiting_sync_tasks.append(data)
                return False
            if sync:
                self._executing_sync_task = True
        queue = self.q()
        thread = threading.Thread(target=self._executor,
                                  args=(queue, host, args,
                                        kwargs,
                                        upstream_exception_handler),
                                  daemon=True)
        thread.start()
        self._short_loop(queue, consumer, unpack_result,
                         upstream_exception_handler,
                         downstream_exception_handler)
        return True

    def _consume(self, queue, consumer, unpack_result,
                exception_handler, latency):
        if queue is None:
            return
        self._internal_count += 1
        qid = self._internal_count
        data = dict()
        data["queue"] = queue
        data["active"] = True
        data["consumer"] = consumer
        data["unpack_result"] = unpack_result
        data["exception_handler"] = exception_handler
        data["latency"] = latency
        self._queues[qid] = data
        self._loop(qid)
        return qid

    def _executor(self, queue, host, args, kwargs, exception_handler):
        result = None
        exception = None
        exception_occurred = False
        try:
            result = host(*args, **kwargs)
        except Exception as e:
            exception_occurred = True
            exception = e
        if not exception_occurred:
            queue.put(result)
        elif exception_occurred and exception_handler is not None:
            queue.put(None)
            queue.put(exception)
        else:
            raise exception

    def _loop(self, qid):
        if not self._is_valid_qid(qid):
            return
        data = self._queues[qid]
        if not data["active"]:
            return
        queue = data["queue"]
        consumer = data["consumer"]
        unpack_result = data["unpack_result"]
        exception_handler = data["exception_handler"]
        latency = data["latency"]
        if not queue.empty():
            result = queue.get()
            self._dispatch_result(result, consumer, unpack_result, exception_handler)
        next_call = lambda self=self, qid=qid: self._loop(qid)
        self._tk.after(latency, func=next_call)

    def _short_loop(self, queue, consumer,
                    unpack_result,
                    upstream_exception_handler,
                    downstream_exception_handler):
        if not queue.empty():
            self._exec_next_sync_task()
            result = queue.get()
            exception = None
            if not queue.empty():
                exception = queue.get()
            if exception is not None:
                self._dispatch_exception(exception, upstream_exception_handler)
            elif exception is None and consumer is not None:
                self._dispatch_result(result, consumer,
                                      unpack_result,
                                      downstream_exception_handler)
        else:
            next_call = (lambda self=self, queue=queue, consumer=consumer,
                            unpack_result=unpack_result,
                            upstream_exception_handler=upstream_exception_handler,
                            downstream_exception_handler=downstream_exception_handler:
                                self._short_loop(queue, consumer,
                                                 unpack_result,
                                                 upstream_exception_handler,
                                                 downstream_exception_handler))
            self._tk.after(5, next_call)

    def _dispatch_result(self, result, consumer, unpack_result, exception_handler):
        if consumer is not None:
            try:
                self._exec_consumer(consumer, result, unpack_result)
            except Exception as e:
                if exception_handler is not None:
                    try:
                        exception_handler(e)
                    except Exception as e:
                        raise e
                else:
                    raise e

    def _dispatch_exception(self, exception, exception_handler):
        if exception_handler is not None:
            try:
                exception_handler(exception)
            except Exception as e:
                raise e
        else:
            raise exception

    def _exec_next_sync_task(self):
        self._executing_sync_task = False
        if self._waiting_sync_tasks:
            data = self._waiting_sync_tasks[0]
            del self._waiting_sync_tasks[0]
            self._task(data["host"], data["args"], data["kwargs"],
                       data["consumer"], data["sync"],
                       data["unpack_result"], data["upstream_exception_handler"],
                       data["downstream_exception_handler"])


    def _is_valid_qid(self, qid):
        with self._queues_lock:
            if qid is not None and qid in self._queues:
                return True
            return False

    def _exec_consumer(self, consumer, result, unpack_result):
        if not unpack_result:
            collections.Sequence
            consumer(result)
            return
        if isinstance(result, dict):
            consumer(**result)
        elif isinstance(result, collections.Sequence):
            consumer(*result)
        else:
            consumer(result)
