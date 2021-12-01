import multiprocessing
#import uvicorn

import sys
sys.path.append('..')
import objstore
print(dir(objstore))

PORT = 8654
HOST = 'localhost'

def server_process(host, port):
    '''Function to be run in the process.
    '''
    objstore.run(host=host, port=port)

def test_basics():
    # launch server process
    #p = multiprocessing.Process(target=server_process, args=(HOST, PORT))
    #p.run()

    # make client object
    with multiprocessing.Process(target=server_process, args=(HOST, PORT)) as p:
        client = objstore.Client(HOST, port=PORT)
        assert(client.status()['running'])
    #p.terminate()
    exit()
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











