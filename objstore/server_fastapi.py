from typing import Optional

import fastapi

app = fastapi.FastAPI()


@app.get("/status")
async def status():
    return {"live": True}

@app.get("/repos")
async def repos():
    return ['a', 'b', 'c']

@app.get("/repo/{repo_name}")
async def data(repo_name: str):
    return repo_name

@app.put("/repo/{repo_name}", response_model=bytes)
async def data(repo_name: str, data: bytes):
    return data


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



