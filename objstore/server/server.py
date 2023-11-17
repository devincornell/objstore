from typing import Optional, Any
import pickle
import pathlib
import fastapi
import io

from ..errors import RepoDoesNotExist, KeyDoesNotExist
from .repodata import RepoData

def data_from_request(request: fastapi.Request) -> RepoData:
    '''Return repodata from app state.
    '''
    return request.app.state.repodata

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
    rdata = data_from_request(request)
    return {
        "is_alive": True, 
        'num_repos': len(rdata),
        'num_items': rdata.num_items(),
    }

@app.get("/repositories/list")
async def list_repos(request: fastapi.Request):
    '''List repositories on the server.
    '''
    return data_from_request(request).list_repos()

@app.post("/repositories/new", status_code=201)
async def make_repo(request: fastapi.Request, repo_name: str):
    '''Make a new repository.
    '''
    data_from_request(request).make_repo(repo_name)


############## manage repositories ##############

@app.get("/repositories/repo/{repo_name}/keys")
async def get_repo_keys(request: fastapi.Request, repo_name: str):
    '''Get list of keys in the repository.
    '''
    return list(data_from_request(request).get_data(repo_name).keys())

@app.get("/repositories/repo/{repo_name}/delete")
async def delete_repo(request: fastapi.Request, repo_name: str):
    '''Delete the given repository.
    '''
    data_from_request(request).delete_repo(repo_name)
    return {'success': True}


############## manage data in repositories ##############

@app.get("/repositories/repo/{repo_name}/data")
async def get_data(request: fastapi.Request, repo_name: str, key: Optional[str] = None):
    '''Get all (when key is None) or specific data from an existing repository.
    '''
    data = pickle.dumps(data_from_request(request).get_data(repo_name, key=key))
    return fastapi.responses.StreamingResponse(io.BytesIO(data))

@app.put("/repositories/repo/{repo_name}/data", status_code=201)
async def put_data(request: fastapi.Request, repo_name: str, key: str, file: fastapi.UploadFile = fastapi.File(None)):
    ''''Store data in a repository.
    '''
    data_from_request(request).put_data(repo_name, key, pickle.load(file.file))
    return {'success': True}

@app.delete("/repositories/repo/{repo_name}/data")
async def delete_data(request: fastapi.Request, repo_name: str, key: str):
    '''Delete repository or specific data.
    '''
    data_from_request(request).delete_data(repo_name, key)
    return {'success': True}
