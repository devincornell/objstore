

import objstore

if __name__ == '__main__':
    objstore.run_server(
        host ='localhost', 
        port = 8000, 
        log_level = 'info'
    )