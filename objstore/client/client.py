
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

    def __init__(self, host: str, port: int, check_connection: bool = True):
        self.host = host if host.startswith('http://') else f'http://{host}'
        self.port = port

        # try to get status from server. if a connection issue, exception will be raised
        if check_connection:
            self.status()
    
    @property
    def urlbase(self):
        return f'{self.host}:{self.port}'

    def status(self, **request_kwargs):
        response = self.request('get', 'repositories/status', **request_kwargs)
        return response.json()

    def list_repos(self, **request_kwargs):
        '''Request a list of repositories from the server.
        '''
        response = self.request('get', 'repositories/list', **request_kwargs)
        return response.json()

    def make_repo(self, repo_name: str, **request_kwargs):
        '''Make a new repository on the server.
        '''
        params = {'repo_name': repo_name}
        return self.request('post', 'repositories/new', params=params, **request_kwargs)

    def get_repo(self, repo_name: str):
        '''Get a repository object.
        '''
        return Repository(self, repo_name)
    
    def request(self, method, endpoint, **request_kwargs):
        '''Make request and return response from server.
        '''
        url = f'{self.urlbase}/{endpoint}'
        response = self.method_funcs[method.lower()](url, **request_kwargs)
        
        if response.status_code != 200:
            
            # try to modify reason before raising exception
            # see how the .raise_for_status() implementation uses self.reason
            # https://docs.python-requests.org/en/latest/_modules/requests/models/#Response.raise_for_status
            try:
                response.reason = response.json()
            except:
                pass
            response.raise_for_status()
        else:
            return response




