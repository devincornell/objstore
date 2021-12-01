
import dataclasses
import werkzeug

class RepoDoesNotExist(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class RepoAlreadyExists(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class KeyDoesNotExist(BaseException):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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






