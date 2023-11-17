
import dataclasses
import urllib
import pickle
import json
import typing
import io

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
        endpoint = f'repositories/repo/{self.name}/keys'
        response = self.client.request('get', endpoint, **request_kwargs)
        return response.json()
    
    def get_all(self, **request_kwargs):
        '''Get all data in the repository. May take a long time.
        '''
        endpoint = f'repositories/repo/{self.name}'
        
        # process args and make request
        response = self.client.request('GET', endpoint, stream=True, **request_kwargs)
        
        # handle response
        return pickle.load(response.raw)

    def get_data(self, key: str, **request_kwargs):
        '''Download specific data from the server.
        '''
        endpoint = f'repositories/repo/{self.name}/data'
        # process args and make request
        request_kwargs['params'] = {**request_kwargs.get('params',{}), **{'key': key}}
        response = self.client.request('GET', endpoint, stream=True, **request_kwargs)
        return pickle.loads(response.content)

    def put_data(self, key: str, data: typing.Any, **request_kwargs):
        '''Upload data to the server.
        '''
        endpoint = f'repositories/repo/{self.name}/data'

        # update key
        request_kwargs['params'] = {**request_kwargs.get('params',{}), 'key': key}
        
        # prepare file data
        files = {'file': pickle.dumps(data)}

        response = self.client.request('put', endpoint, stream=True, files=files, **request_kwargs)
        return response
