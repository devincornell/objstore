import uvicorn
import argparse
from .server import app

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()

    # just copied from these docs:
    # https://www.uvicorn.org/#running-programmatically
    parser.add_argument('-p', '--port', help='Port to listen on.', type=int, default=8000)
    parser.add_argument('--host', help='Hostname to listen on.', type=str, default='localhost')
    parser.add_argument('-l', '--log_level', help='Log level.', type=str, default='info')
    #parser.add_argument('-r', '--reload', help='Reload when server code is changed?', action='store_true')
    args = parser.parse_args()

    uvicorn.run(app, **vars(args))

