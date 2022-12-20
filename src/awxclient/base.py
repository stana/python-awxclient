import json

from awxclient import exception

class BaseManager(object):
    def __init__(self, conn, rel_url_base):
        self._conn = conn
        self._relative_url_base = rel_url_base

    def get_all(self, **kwargs):
        # example kwargs could be {'page':2}
        return self._conn.get(self._relative_url_base, query_params=kwargs)

    def _get_id_url(self, object_id):
        return f"{self._relative_url_base}/{object_id}"

    def get_by_id(self, object_id):
        id_url = self._get_id_url(object_id)
        resource = self._conn.get(id_url)
        return resource

    def get_by_name(self, name):
        params = {"name": name}
        result = self._conn.get(self._relative_url_base, query_params=params)
        if result and result.get('count'):
            return result['results'][0]
        raise exception.AWXClientRequestException(status=404, message={"detail": "Not found."})

    def search(self, search_term):
        params = {"search": search_term}
        return self._conn.get(self._relative_url_base, query_params=params)

    def search_by_field(self, field_name, field_val):
        params = {f"{field_name}__search": field_val}
        return self._conn.get(self._relative_url_base, query_params=params)

    def create(self, json=None, data=None):
        return self._conn.post(self._relative_url_base, json=json, data=data)

    def update(self, object_id, json=None, data=None):
        return self._conn.put(self._get_id_url(object_id), json=json, data=data)

    def delete(self, object_id):
        return self._conn.delete(self._get_id_url(object_id))
