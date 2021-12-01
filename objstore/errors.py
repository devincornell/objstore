
import dataclasses
import werkzeug
import fastapi

# this page shows how error handling works
# https://fastapi.tiangolo.com/tutorial/handling-errors/

class ObjStoreBaseException(fastapi.HTTPException):
    '''Each inheriting class must provide status_code and message properties for the http response.
    '''
    verbose = True
    def __init__(self, *args, **kwargs):
        if self.verbose: print(self.message)
        super().__init__(*args, status_code=self.status_code, detail=self.message, **kwargs)

class RepoAlreadyExists(ObjStoreBaseException):
    status_code = 409
    def __init__(self, repo_name: str, *args, **kwargs):
        self.repo_name = repo_name
        super().__init__(*args, **kwargs)

    @property
    def message(self):
        return (f'The repository "{self.repo_name}" already exists on the server'
            ' - cannot create it twice.')

class RepoDoesNotExist(ObjStoreBaseException):
    status_code = 404
    def __init__(self, repo_name: str, *args, **kwargs):
        self.repo_name = repo_name
        super().__init__(*args, **kwargs)

    @property
    def message(self):
        return f'The repository "{self.repo_name}" does not exist on the server.'


class KeyDoesNotExist(ObjStoreBaseException):
    status_code = 404
    def __init__(self, repo_name: str, key_name: str, *args, **kwargs):
        self.repo_name = repo_name
        self.key_name = key_name
        super().__init__(*args, **kwargs)

    @property
    def message(self):
        return f'The data "{self.key_name}" does not exist in repository "{self.repo_name}".'

@dataclasses.dataclass
class Error:
    name: str
    code: int
    exception: Exception
    message: str = None

    def reply(self):
        '''Data to be sent from the server to the client through Flask.
        '''
        return self.message, self.code

    def raise_exception(self):
        '''Raise the exception on the client side.
        '''
        if self.message is not None:
            raise self.exception(self.message)
        else:
            raise self.exception()
    
# this is a list of custom errors that can be provided by the server
error_list = [
    Error('key_not_provided', 460, werkzeug.exceptions.BadRequest, 'A key parameter must be provided when putting or accessing this resource.'),
    Error('repository_not_found', 461, KeyError, 'The specified repository was not found on the server.'),
    Error('data_not_found', 462, KeyError, 'The requested data key was not found on the repository.'),
    Error('no_data_received', 462, KeyError, 'No data was included in PUT request.'),
]

names = {e.name: e for e in error_list}
codes = {e.code: e for e in error_list}



class ServerNotLive(BaseException):
    pass

class CouldNotContactServer(BaseException):
    pass






