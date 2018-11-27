import argparse
import json
import os
import requests


class Firebase:

    ROOT_URL = ''  # no trailing slash

    def __init__(self, root_url, auth_token=None):
        self.ROOT_URL = root_url.rstrip('/')
        self.auth_token = auth_token

    # These mirror REST API functionality

    def put(self, node, data):
        return self.__request('put', node=node, data=data)

    def patch(self, node, data):
        return self.__request('patch', node=node, data=data)

    def get(self, node, params=None):
        return self.__request('get', node=node, data=params)

    def post(self, node, data):
        return self.__request('post', node=node, data=data)

    def delete(self, node):
        return self.__request('delete', node=node)

    # Private

    def __request(self, method, **kwargs):
        # Firebase API does not accept form-encoded PUT/POST data. It needs to
        # be JSON encoded.
        node = kwargs.get("node", "/")
        if "node" in kwargs:
            del kwargs["node"]

        if 'data' in kwargs:
            kwargs['data'] = json.dumps(kwargs['data'])

        params = {}
        if self.auth_token:
            if 'params' in kwargs:
                params = kwargs['params']
                del kwargs['params']
            params.update({'auth_token': self.auth_token})

        r = requests.request(method, self.__url(node), params=params, **kwargs)
        r.raise_for_status()  # throw exception if error
        return r.json()

    def __url(self, node):
        # We append .json to end of ROOT_URL for REST API.
        return '{0}.json'.format(self.ROOT_URL + node)