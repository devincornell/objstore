
import dataclasses
import urllib
import pickle
import json
from ..errors import RepoDoesNotExist

class Repository:

    def __init__(self, client, repo_name: str, **make_repo_kwargs):
        self.name = repo_name
        self.client = client

        # make the repository if it does not exist
        if self.name not in self.client.list_repos():
            self.client.make_repo(self.name, **make_repo_kwargs)

    def list_keys(self, **request_kwargs):
        '''Get the data keys associated with this repository.
        '''
        response = self.client.request('get', f'repositories/{self.name}/keys', **request_kwargs)
        return response.json()
    
    def get_all(self, **request_kwargs):
        '''Get all data in the repository. May take a long time.
        '''
        response = self.client.request(f'data/{self.name}', 'GET', stream=True, **request_kwargs)
        return pickle.load(response.raw)

    def get_data(self, key: str, **request_kwargs):
        '''Download specific data from the server.
        '''
        # process args and make request
        request_kwargs['params'] = {**request_kwargs.get('params',{}), **{'key': key}}
        response = self.client.request('GET', f'repositories/repo/{self.name}', stream=True, **request_kwargs)
        
        # handle response
        return pickle.load(response.raw)

    def put_data(self, key, payload, **request_kwargs):
        '''Upload data to the server.
        '''
        data = pickle.dumps(payload)
        params = {'key': key}
        response = self.client.request(f'data/{self.name}', 'PUT', data=data, params=params, stream=True, **request_kwargs)
        return response