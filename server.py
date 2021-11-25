import pickle
import flask
import io
import errors
import flask_restful
#from flask_restful import Api
#from flask_restful_swagger import swagger

app = flask.Flask(__name__)
api = flask_restful.Api(app)

data_store = {
    'userdata': {
        'users': [
            {'name': 'Devin', 'age': range(10)},
            {'name': 'Aaron', 'age': range(10)},
            {'name': 'Richard', 'age': range(500)},
        ]
    }
}


class Status(flask_restful.Resource):
    '''Request the status of the server.
    '''
    def get(self):
        num_elements = len([k for repo in data_store.values() for k in repo])
        return flask.jsonify({'live': True, 'num_repos': len(data_store), 'num_elements': num_elements})

api.add_resource(Status, '/status')

class Repositories(flask_restful.Resource):
    '''Access information about the repositories.
    '''
    def get(self):
        return flask.jsonify(list(data_store.keys()))

api.add_resource(Repositories, '/data')


class Data(flask_restful.Resource):
    def get(self, repository: str):

        # make sure the repository exists
        try:
            repo = data_store[repository]
        except KeyError as e:
            return errors.names['repository_not_found'].reply()

        # either send entire repository or get specific element
        if 'key' not in flask.request.args:
            return self.send_data(repo)
        
        else:
            key = flask.request.args['key']
            try:
                data = repo[key]
            except KeyError:
                return errors.names['data_not_found'].reply()

            return self.send_data(data, key)

        if 'key' not in flask.request.args:
            return errors.names['key_not_provided'].reply()
        
        key = flask.request.args['key']
        if key not in data_store:
            return errors.names['key_not_found'].reply()

        data = data_store.setdefault(key, dict())
        
        payload = io.BytesIO(pickle.dumps(data_store[key]))
        
        return flask.send_file(payload)

    def put(self, repository: str):
        '''Receive and store data.
        '''
        
        # retrieve the data that was sent
        print(flask.request.args)
        print(flask.request.form)
        data = pickle.loads(flask.request.get_data())
        try:
            key = flask.request.args['key']
        except KeyError:
            return errors.names['key_not_provided'].reply()
        
        # make the repo if it doesn't exist already
        repo = data_store.setdefault(repository, dict())
        repo[key] = data

        return flask.jsonify({'success': True})

    @classmethod
    def send_data(cls, data, key: str = 'data'):
        '''Send data using flask.
        '''
        payload = io.BytesIO(pickle.dumps(data))
        return flask.send_file(payload, attachment_filename=key)

api.add_resource(Data, '/data/<string:repository>')


class DataKeys(flask_restful.Resource):
    def get(self, repository: str):

        # make sure the repository exists
        try:
            repo = data_store[repository]
        except KeyError as e:
            return errors.names['repository_not_found'].reply()

        return flask.jsonify(list(repo.keys()))

api.add_resource(DataKeys, '/data/<string:repository>/keys')

#@app.route('/hello/', methods=['GET', 'POST'])
#def welcome():
#    return "Hello World!"
#
#@app.route('/data', methods=['GET'])
#def data_endpoint():
#    print(flask.request.method)
#    # user is requesting data
#    if flask.request.method == 'GET':
#        print('handling GET request')
#        if 'key' not in flask.request.args:
#            return errors['key_not_provided'].reply()
#        
#        key = flask.request.args['key']
#        if key not in data_store:
#            return errors['data_not_found'].reply()
#        
#        payload = io.BytesIO(pickle.dumps(data_store[key]))
#        
#        return flask.send_file(payload)
#    
#    # user is uploading data
#    elif flask.request.method == 'PUT':
#        print('handling PUT request')
#        key = flask.request.args['key']
#        raw_data = flask.request.get_data()
#
#        replaced = key in data_store
#        data_store[key] = pickle.loads(raw_data)
#        return flask.jsonify({
#            'replaced': replaced, 
#            'key': key, 
#            'data_size': len(raw_data),
#        })

if __name__ == '__main__':
    app.run(host='localhost', port=9999)


