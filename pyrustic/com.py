from pyrustic.exception import PyrusticException


class Com:
    """ work in progress """
    def __init__(self, tk=None, event_sep=" "):
        self._tk = tk
        self._event_sep = event_sep
        self._i = 0
        self._subscriptions = dict()
        self._subscribers = dict()
        self._resources = dict()

    @property
    def tk(self):
        return self._tk

    @tk.setter
    def tk(self, val):
        self._tk = val

    @property
    def event_sep(self):
        return self._event_sep

    @property
    def subscribers(self):
        return self._subscribers.copy()

    @property
    def resources(self):
        return self._resources.copy()

    def pub(self, event, data=None, sync=False):
        event_seq = self._split(event)
        if not event_seq:
            raise PyrusticException("Please submit a correct event")
        if "" in self._subscriptions:
            sid_set = self._subscriptions[""]
            self._release_to_sid_set(sid_set, event, data, sync)
        for sid_set in self._seq_loop(event_seq):
            self._release_to_sid_set(sid_set, event, data, sync)

    def sub(self, event, consumer):
        if consumer is None:
            return None
        event_seq = self._split(event)
        if not event_seq:
            if not "" in self._subscriptions:
                self._subscriptions[""] = set()
            self._register_consumer(self._subscriptions[""], consumer)
        else:
            last_sid_set = None
            for sid_set in self._seq_loop(event_seq):
                last_sid_set = sid_set
            self._register_consumer(last_sid_set, consumer)

    def unsub(self, sid):
        if not sid in self._subscribers:
            return False
        del self._subscribers[sid]
        return True

    def event_handler(self, instance, prefix="_on_"):
        event_handler_map = {}
        for attr in dir(instance):
            if attr.startswith(prefix):
                event = self._convert_attr_into_event(attr, prefix)
                event_handler_map[event] = getattr(instance, attr)
        consumer = \
            (lambda event, data, event_handler_map=event_handler_map:
                event_handler_map[event](event, data)
                    if event in event_handler_map else None)

        return self.sub(None, consumer=consumer)

    def res(self, name, handler):
        self._resources[name] = handler

    def unres(self, name):
        if not name in self._resources:
            return False
        del self._resources[name]
        return True

    def req(self, resource, res_args=None,
            res_kwargs=None, consumer=None,
            sync=False):
        if not resource in self._resources:
            raise PyrusticException("Missing resource: {}".format(resource))
        res_args = tuple() if not res_args else res_args
        res_kwargs = dict() if not res_kwargs else res_kwargs
        handler = self._resources[resource]
        command = (lambda handler=handler,
                          res_args=res_args,
                          res_kwargs=res_kwargs:
                                handler(*res_args, **res_kwargs))
        if sync or not self._tk:
            command()
        else:
            self._tk.after(0, command)

    def _split(self, event):
        if not event or not isinstance(event, str):
            return None
        return event.split(self._event_sep)

    def _gen_sid(self):
        self._i += 1
        return self._i

    def _register_consumer(self, sid_set, consumer):
        sid = self._gen_sid()
        sid_set.add(sid)
        self._subscribers[sid] = consumer

    def _seq_loop(self, event_seq):
        cache = self._subscriptions
        for index, item in enumerate(event_seq):
            sid_set = None
            for i in range(index, index + 1):
                if item not in cache:
                    cache[item] = dict()
                if "" not in cache[item]:
                    cache[item][""] = set()
                sid_set = cache[item][""]
                cache = cache[item]
                yield sid_set

    def _release_to_sid_set(self, sid_set, event,
                            data, sync):
        for sid in sid_set:
            consumer = self._subscribers.get(sid, None)
            if consumer is None:
                continue
            self._release(event, data,
                          consumer, sync)

    def _release(self, event, data, consumer, sync):
        command = (lambda consumer=consumer,
                          event=event,
                          data=data:
                                consumer(event, data))
        if sync or not self._tk:
            command()
        else:
            self._tk.after(0, command)

    def _dispatch(self, event, data, event_handler_map):
        handler = event_handler_map.get(event, None)
        if handler:
            handler(event, data)

    def _convert_attr_into_event(self, attr, prefix):
        cache = attr.lstrip(prefix)
        return cache.replace("_", self._event_sep)
