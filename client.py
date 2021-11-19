
import requests
import dataclasses
import urllib
import pickle
from errors import errors

class DataStoreClient:
    method_funcs = {
        'POST': requests.post,
        'GET': requests.get,
        'PUT': requests.put,
    }
    def __init__(self, host, port):
        self.host = host if host.startswith('http://') else f'http://{host}'
        self.urlbase = f'{self.host}:{port}'

    def get_data(self, key, **request_params):
        # process args and make request
        request_params['params'] = {**request_params.get('params',{}), **{'key': key}}
        response = self.request('data', 'GET', stream=True, **request_params)
        
        # handle response
        if response.status_code == 200:
            return pickle.load(response.raw)
        elif response.status_code == 460:
            raise KeyError(response.text)

    def put_data(self, key, payload, **request_params):
        # process args and make request
        request_params['params'] = {**request_params.get('params',{}), **{'key': key}}
        response = self.request('data', 'PUT')#, data={'payload': pickle.dumps(payload)})
        return response
        # handle response
        #if response.status_code == 200:
        #    return True
        #else:
        #    return False


    def request(self, endpoint, method: str = 'GET', **request_kwargs):
        response = self.method_funcs[method](f'{self.urlbase}/{endpoint}', **request_kwargs)
        if response.status_code in errors:
            errors[]
        else:
            return response


if __name__ == '__main__':
    client = DataStoreClient('localhost', 9999)
    print(client.host)
    #res = requests.get('http://localhost:9999/hello?stop=5')
    #print(client.request('range', params={'stop':5}).json())
    
    #print(client.request('data', 'GET', params={'key':'duh'}))
    #print(client.request('hello', 'PUT'))
    #print(client.request('hello', 'POST'))
    #print(client.request('hello', 'GET'))
    
    
    
    print(client.get_data('namez'))
    #print(client.put_data('age', 4))


