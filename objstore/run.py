import uvicorn
from .server import app

def run(*args, **kwargs):
    '''Run the uvicorn app.
    '''
    uvicorn.run(app, *args, **kwargs)
