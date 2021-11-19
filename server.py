import pickle
import flask
import io
from errors import errors
#from flask_restful import Api
#from flask_restful_swagger import swagger

app = flask.Flask(__name__)
#api = Api(app)

data_store = {'name': 'Devin', 'age': range(10)}

@app.route('/hello/', methods=['GET', 'POST'])
def welcome():
    return "Hello World!"

@app.route('/data', methods=['GET', 'PUT'])
def data_endpoint():
    print(flask.request.method)
    # user is requesting data
    if flask.request.method == 'GET':
        print('handling GET request')
        if 'key' not in flask.request.args:
            return errors['key_not_provided'].reply()
        
        key = flask.request.args['key']
        if key not in data_store:
            return errors['data_not_found'].reply()
        
        payload = io.BytesIO(pickle.dumps(data_store[key]))
        return flask.send_file(payload)
    
    # user is uploading data
    elif flask.request.method == 'PUT':
        print('handling PUT request')
        key = flask.request.args['key']
        raw_data = flask.request.get_data()

        replaced = key in data_store
        data_store[key] = pickle.loads(raw_data)
        return flask.jsonify({
            'replaced': replaced, 
            'key': key, 
            'data_size': len(raw_data),
        })

if __name__ == '__main__':
    app.run(host='localhost', port=9999)


