
import requests
import dataclasses
import urllib
import pickle
import json
import errors
import io

class Client:
    method_funcs = {
        'POST': requests.post,
        'GET': requests.get,
        'PUT': requests.put,
    }

    def __init__(self, host: str, port: int, test: bool = True):
        self.host = host if host.startswith('http://') else f'http://{host}'
        self.port = port

        # try to get status from server. if a connection issue, it will be raised
        # if another error, 
        if not self.status()['live']:
            raise errors.ServerNotLive('The server replied that it is not live!')
    
    @property
    def urlbase(self):
        return f'{self.host}:{self.port}'

    def status(self, **request_kwargs):
        response = self.request('status', 'GET', **request_kwargs)
        return response.json()

    def list_repos(self, **request_kwargs):
        '''Request a list of repositories from the server.
        '''
        response = self.request('data', 'GET', **request_kwargs)
        return response.json()

    def get_repo(self, repo_name: str):
        '''Get a repository object.
        '''
        return Repository(self, repo_name)
    
    def request(self, endpoint, method: str = 'GET', **request_kwargs):
        '''Make request and return response from server.
        '''
        url = f'{self.urlbase}/{endpoint}'
        response = self.method_funcs[method](url, **request_kwargs)
        
        if response.status_code in errors.codes:
            raise errors.codes[response.status_code].raise_exception()
        else:
            response.raise_for_status()
            return response

class Repository:

    def __init__(self, client: Client, name: str = 'default_repository'):
        self.name = name
        self.client = client

    def get_keys(self, **request_kwargs):
        '''Get the data keys associated with this repository.
        '''
        response = self.client.request(f'data/{self.name}/keys', 'GET', **request_kwargs)
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
        response = self.client.request(f'data/{self.name}', 'GET', stream=True, **request_kwargs)
        
        # handle response
        return pickle.load(response.raw)

    def put_data(self, key, payload, **request_kwargs):
        '''Upload data to the server.
        '''
        data = pickle.dumps(payload)
        params = {'key': key}
        response = self.client.request(f'data/{self.name}', 'PUT', data=data, params=params, stream=True, **request_kwargs)
        return response


if __name__ == '__main__':
    client = Client('localhost', port=9999)
    #print(client.host)
    print(client.list_repos())
    print(client.status())
    
    user_repo = client.get_repo('userdata')
    print(user_repo.get_keys())
    print(user_repo.get_data('users'))
    print(user_repo.get_all())
    user_repo.put_data('friends', 'list of my friends')
    print(user_repo.get_keys())
    print(user_repo.get_data('friends'))

    #other_repo = client.get_repo('others')
    #other_repo.get_data()
    #res = requests.get('http://localhost:9999/hello?stop=5')
    #print(client.request('range', params={'stop':5}).json())
    
    #print(client.request('data', 'GET', params={'key':'duh'}))
    #print(client.request('hello', 'PUT'))
    #print(client.request('hello', 'POST'))
    #print(client.request('hello', 'GET'))
    
    
    
    #print(client.get_data('namez'))
    #print(client.put_data('age', 4))


