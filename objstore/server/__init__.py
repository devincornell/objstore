
#from .repodata import RepoData
from .server import app
from .repodata import RepoData
#from .server import app

import uvicorn
def run_server(
    host: str = 'localhost', 
    port: int = 8000, 
    log_level: str = 'info'
) -> None:
    '''Run the uvicorn server.'''
    return uvicorn.run(
        app, 
        host=host,
        port=port,
        log_level=log_level,
    )


