import threading
import collections
import queue


class Threadom:
    def __init__(self, tk, sync=False):
        """
        - tk: a tk.Tk instance or any tkinter object
        - sync: boolean
        """
        self._tk = tk
        self._sync = sync
        self._internal_count = 0
        self._queues = dict()
        self._queues_lock = threading.Lock()
        self._running_synced_target_lock = threading.Lock()
        self._waiting_synced_target_to_run = list()
        self._running_synced_target = False


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

        - queue: the queue. See Threadom's method 'q'.
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

    def info(self, qid=None):
        """
        Retrieve info from the process launched by the method 'consume'.
        Returns a dict:
         {"queue": queue, "active": boolean, "consumer": callback, "unpack_result": boolean,
         "exception_handler": callback, "latency": integer}
        """
        if qid is None:
            with self._queues_lock:
                return tuple([x.copy() for x in self._queues])
        if not self._is_valid_qid(qid):
            return
        with self._queues_lock:
            return self._queues[qid].copy()

    def run(self, target, target_args=None,
            target_kwargs=None,
            consumer=None,
            sync=None,
            daemon=True,
            unpack_result=False,
            upstream_exception_handler=None,
            downstream_exception_handler=None):
        """
        Runs a target in background. Return False if the target is in WAITING state (sync)
        - target: the callable to run
        - target_args: tuple, arguments to use
        - target_kwargs: dict, keyword-arguments to use
        - consumer: the callback with parameter(s) that will consume the returned value by target
        - sync: None or boolean to override the constructor's argument sync
        - unpack_result: boolean, True, to unpack the result returned by target
        - upstream_exception_handler: one parameter callback to handle the exception
            raised while running the target
        - downstream_exception_handler: one parameter callback to handle the exception
            raised while calling the consumer
        """
        sync = self._sync if sync is None else sync
        target_args = {} if target_args is None else target_args
        target_kwargs = {} if target_kwargs is None else target_kwargs
        return self._run(target, target_args,
                         target_kwargs, consumer,
                         sync, daemon, unpack_result,
                         upstream_exception_handler,
                         downstream_exception_handler)

    # ===========================================
    #               INTERNAL
    # ===========================================

    def _run(self, target, target_args,
             target_kwargs, consumer,
             sync, daemon, unpack_result,
             upstream_exception_handler,
             downstream_exception_handler):
        if sync:
            with self._running_synced_target_lock:
                if self._running_synced_target:
                    data = {"target": target,
                            "target_args": target_args,
                            "target_kwargs": target_kwargs,
                            "consumer": consumer,
                            "sync": sync, "daemon": daemon,
                            "unpack_result": unpack_result,
                            "upstream_exception_handler":
                                upstream_exception_handler,
                            "downstream_exception_handler":
                                downstream_exception_handler}
                    self._waiting_synced_target_to_run.append(data)
                    return False
                self._running_synced_target = True
        queue = self.q()
        thread = threading.Thread(target=self._runner,
                                  args=(queue, target, target_args,
                                        target_kwargs,
                                        upstream_exception_handler),
                                  daemon=daemon)
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

    def _runner(self, queue, target, target_args, target_kwargs, exception_handler):
        result = None
        exception = None
        exception_occurred = False
        try:
            result = target(*target_args, **target_kwargs)
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
            if result is QueueTail:
                return
        next_call = lambda self=self, qid=qid: self._loop(qid)
        self._tk.after(latency, func=next_call)

    def _short_loop(self, queue, consumer,
                    unpack_result,
                    upstream_exception_handler,
                    downstream_exception_handler):
        if not queue.empty():
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
            self._run_next_synced_target()
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
                self._run_consumer(consumer, result, unpack_result)
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

    def _run_next_synced_target(self):
        self._running_synced_target = False
        if self._waiting_synced_target_to_run:
            data = self._waiting_synced_target_to_run[0]
            del self._waiting_synced_target_to_run[0]
            self._run(data["target"], data["target_args"], data["target_kwargs"],
                      data["consumer"], data["sync"], data["daemon"],
                      data["unpack_result"], data["upstream_exception_handler"],
                      data["downstream_exception_handler"])

    def _is_valid_qid(self, qid):
        with self._queues_lock:
            if qid is not None and qid in self._queues:
                return True
            return False

    def _run_consumer(self, consumer, result, unpack_result):
        if unpack_result and isinstance(result, dict):
            consumer(**result)
        elif unpack_result and isinstance(result, collections.Sequence):
            consumer(*result)
        else:
            consumer(result)


class QueueTail:
    pass
