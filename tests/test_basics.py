import multiprocessing
import subprocess
#import uvicorn

import sys

from requests.models import HTTPError
sys.path.append('..')
import objstore

PORT = 8000
HOST = 'localhost'


def test_basics():
    
    client = objstore.Client(HOST, PORT)
    status = client.status()
    assert(status['is_alive'])
    
    assert(status['num_repos'] == 0)
    assert(status['num_items'] == 0)
    assert(client.list_repos() == [])

    repo = client.get_repo('new_repo')
    assert(len(client.list_repos()) == 1)
    assert(repo.list_keys() == [])
    
    print(repo.put_data('a', range(10)))
    print(list(repo.get_data('a')))
    print(repo.list_keys())



if __name__ == '__main__':
    test_basics()











