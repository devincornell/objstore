import multiprocessing
import subprocess
#import uvicorn

import sys

from requests.models import HTTPError
sys.path.append('..')
import objstore

PORT = 8000
HOST = 'localhost'


def test_basics(host: str = HOST, port: int = PORT):
    
    client = objstore.Client(HOST, PORT)
    status = client.status()
    assert(status['is_alive'])
    
    assert(status['num_repos'] == 0)
    assert(status['num_items'] == 0)
    assert(client.list_repos() == [])

    repo = client.get_repo('new_repo')
    assert(len(client.list_repos()) == 1)
    assert(repo.list_keys() == [])
    
    d = range(10)
    repo.put_data('a', d)
    assert(list(repo.get_data('a')) == list(d))
    assert(repo.list_keys() == ['a'])



if __name__ == '__main__':
    test_basics()











