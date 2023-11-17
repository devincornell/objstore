# objstore Package

Client/server for storing/retrieving Python data in RAM.

Created by [Devin J. Cornell](https://devinjcornell.com).

Ideal use conditions:

+ You have a dataset that takes a long time to load into RAM.
+ You can store 3x the object sizes in RAM.


## Installation

`pip install --upgrade git+https://github.com/devincornell/objstore.git@master`

## Docs


### Starting the Server

You can run the server using the following command:

```
python -m objstore server --host localhost --port 8000 --loglevel info
```

Alternatively, you can write a Python script to start the server.

```python
import objstore

if __name__ == '__main__':
    objstore.run_server(
        host ='localhost', 
        port = 8000, 
        log_level = 'info'
    )
```

### Using the Client Interface

The next step is to connect to the server from your application so you can store and retrieve objects. Firstly, you may use the command line to list existing repositories and the data they store.

`python -m objstore list --host localhost --port 8000`

The primary interface for these operations is `Client`, which you can create by calling the constructor with the specified host information. An exception will be raised if there is an issue.

The following example assumes we have started the server in another process on the specified host and port. Use the `status()` command to make sure the server is running.

```python
client = objstore.Client(
    host = 'localhost', 
    port = 8000
)
client.status()
```

The status result will look like this:

```
>> {'is_alive': True, 'num_repos': 1, 'num_items': 1}
```

And the following operations will allow you to submit/receive data from the server.

```python
# list the existing repositories
client.list_repos()

# create a new repo, see that it has been created
repo = client.get_repo('new_repo')
client.list_repos()

# get the keys in the repo (empty now)
repo.list_keys()

# will place the list in storage
d = list(range(10))
repo.put_data('a', d)

# see that the data has been recorded
repo.list_keys()

# access the list
repo.get_data('a')

```



