import multiprocessing
import subprocess
#import uvicorn

import sys

from requests.models import HTTPError
sys.path.append('..')
import objstore

PORT = 8001
HOST = 'localhost'


def test_basics():
    
    
    client = objstore.Client(HOST, PORT)
    assert(client.status()['is_alive'])
    
    
    print(client.status())
    print(client.list_repos())

    repo = client.get_repo('new_repo')
    print(client.list_repos())
    print(repo.list_keys())
    print(repo.put_data('a', range(10)))
    print(list(repo.get_data('a')))
    print(repo.list_keys())



if __name__ == '__main__':
    test_basics()











