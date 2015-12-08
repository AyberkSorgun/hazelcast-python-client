import threading

def check_not_none(val, message):
    if val is None:
        raise AssertionError(message)

class Proxy(object):
    def __init__(self, client, service_name, name):
        self.service_name = service_name
        self.name = name
        self._client = client

    def destroy(self):
        pass
        # TODO

    def __str__(self):
        return '%s(name="%s")' % (type(self), self.name)

    def to_data(self, val):
        return self._client.serializer.to_data(val)

    def to_object(self, data):
        self._client.serializer.to_object(data)

    def thread_id(self):
        return threading.currentThread().ident

    def invoke(self, request):
        return self._client.invoker.invoke_on_random_target(request).result()

    def invoke_on_key(self, request, key_data):
        partition_id = self._client.partition_service.get_partition_id(key_data)
        return self._client.invoker.invoke_on_partition(request, partition_id).result()