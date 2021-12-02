from typing import Optional, Any
import pickle
import pathlib
import fastapi
import io

from ..errors import RepoDoesNotExist, KeyDoesNotExist
from .repodata import RepoData

app = fastapi.FastAPI()



@app.on_event("startup")
async def startup():
    app.state.fname = None
    app.state.repodata = RepoData(app.state.fname)

############################ Repositories Endpoint ############################

@app.get("/repositories/status")
async def status(request: fastapi.Request):
    '''Get the status of the server.
    '''
    return {
        "is_alive": True, 
        'num_repos': len(request.app.state.repodata),
        'num_items': request.app.state.repodata.num_items(),
    }

@app.get("/repositories/list")
async def list_repos(request: fastapi.Request):
    '''List repositories on the server.
    '''
    return list(request.app.state.repodata.list_repos())

@app.post("/repositories/new", status_code=201)
async def make_repo(request: fastapi.Request, repo_name: str):
    '''Make a new repository.
    '''
    repodata = request.app.state.repodata
    repodata.make_repo(repo_name)


############## manage repositories ##############

@app.get("/repositories/repo/{repo_name}/keys")
async def get_repo_keys(request: fastapi.Request, repo_name: str):
    '''Get list of keys in the repository.
    '''
    return list(request.app.state.repodata.get_data(repo_name).keys())

@app.get("/repositories/repo/{repo_name}/delete")
async def delete_repo(request: fastapi.Request, repo_name: str):
    '''Delete the given repository.
    '''
    request.app.state.repodata.delete_repo(repo_name)
    return {'success': True}


############## manage data in repositories ##############

@app.get("/repositories/repo/{repo_name}/data")
async def get_data(request: fastapi.Request, repo_name: str, key: Optional[str] = None):
    '''Get all (when key is None) or specific data from an existing repository.
    '''
    data = pickle.dumps(request.app.state.repodata.get_data(repo_name, key=key))
    return fastapi.responses.StreamingResponse(io.BytesIO(data))

@app.put("/repositories/repo/{repo_name}/data", status_code=201)
async def put_data(request: fastapi.Request, repo_name: str, key: str, file: fastapi.UploadFile = fastapi.File(None)):
    ''''Store data in a repository.
    '''
    request.app.state.repodata.put_data(repo_name, key, pickle.load(file.file))
    return {'success': True}

@app.delete("/repositories/repo/{repo_name}/data")
async def delete_data(request: fastapi.Request, repo_name: str, key: str):
    '''Delete repository or specific data.
    '''
    request.app.state.repodata.delete_data(repo_name, key)
    return {'success': True}
