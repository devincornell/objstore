from typing import Optional, Any
import pickle
import pathlib
import fastapi

from ..errors import RepoDoesNotExist, KeyDoesNotExist
from .repodata import RepoData

app = fastapi.FastAPI()



@app.on_event("startup")
async def startup():
    app.state.fname = None
    app.state.repodata = RepoData(app.state.fname)

@app.get("/repositories/status")
async def status(request: fastapi.Request):
    return {
        "live": True, 
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

#@app.put("/repositories/repo/{repo_name}", status_code=201)
#async def put_data(request: fastapi.Request, repo_name: str, key: str):
#
#    repo = request.app.state.repodata.set_repo(repo_name)

#@app.get("/repositories/repo/{repo_name}/keys")
#async def get_data(request: fastapi.Request, repo_name: str):
#    '''Get list of keys in this repository.
#    '''
#    return list(request.app.state.repodata.get_data(repo_name).keys())

@app.get("/repositories/repo/{repo_name}", response_model=bytes)
async def get_data(request: fastapi.Request, repo_name: str, key: Optional[str] = None):
    '''Get all (when key is None) or specific data from an existing repository.'''
    
    # get either all data or a specific piece of data from the server
    payload = pickle.dumps(request.app.state.repodata.get_data(repo_name, key=key))
    
    return fastapi.Response(content=payload, media_type='application/octet-stream')


#@app.put("/repo/{repo_name}", response_model=bytes)
#async def data(repo_name: str, data: bytes):
#    return data


#class Data(flask_restful.Resource):
#    def get(self, repository: str):
#
#        # make sure the repository exists
#        try:
#            repo = data_store[repository]
#        except KeyError as e:
#            return errors.names['repository_not_found'].reply()
#
#        # either send entire repository or get specific element
#        if 'key' not in flask.request.args:
#            return self.send_data(repo)
#        
#        else:
#            key = flask.request.args['key']
#            try:
#                data = repo[key]
#            except KeyError:
#                return errors.names['data_not_found'].reply()
#
#            return self.send_data(data, key)
#
#
#    def put(self, repository: str):
#        '''Receive and store data.
#        '''
#        
#        # retrieve the data that was sent
#        print(flask.request.args)
#        print(flask.request.form)
#        data = pickle.loads(flask.request.get_data())
#        try:
#            key = flask.request.args['key']
#        except KeyError:
#            return errors.names['key_not_provided'].reply()
#        
#        # make the repo if it doesn't exist already
#        repo = data_store.setdefault(repository, dict())
#        repo[key] = data
#
#        return flask.jsonify({'success': True})
#
#    @classmethod
#    def send_data(cls, data, key: str = 'data'):
#        '''Send data using flask.
#        '''
#        payload = io.BytesIO(pickle.dumps(data))
#        return flask.send_file(payload, attachment_filename=key)



