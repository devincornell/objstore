
import requests
#import errors
import io
from .repository import Repository

class Client:
    method_funcs = {
        'post': requests.post,
        'get': requests.get,
        'put': requests.put,
    }

    def __init__(self, host: str, port: int, test: bool = True):
        self.host = host if host.startswith('http://') else f'http://{host}'
        self.port = port

        # try to get status from server. if a connection issue, it will be raised
        # if another error, 
        if not self.status()['live']:
            #raise errors.ServerNotLive('The server replied that it is not live!')
            pass
    
    @property
    def urlbase(self):
        return f'{self.host}:{self.port}'

    def status(self, **request_kwargs):
        response = self.request('GET', 'status', **request_kwargs)
        return response.json()

    def list_repos(self, **request_kwargs):
        '''Request a list of repositories from the server.
        '''
        response = self.request('GET', 'list_repos', **request_kwargs)
        return response.json()

    def get_repo(self, repo_name: str):
        '''Get a repository object.
        '''
        return Repository(self, repo_name)
    
    def request(self, method, endpoint, **request_kwargs):
        '''Make request and return response from server.
        '''
        url = f'{self.urlbase}/{endpoint}'
        response = self.method_funcs[method.lower()](url, **request_kwargs)
        
        #if response.status_code in errors.codes:
            #raise errors.codes[response.status_code].raise_exception()
        if response.status_code != 200:
            response.raise_for_status()
        else:
            return response




