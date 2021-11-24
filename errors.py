
import dataclasses
import werkzeug

@dataclasses.dataclass
class Error:
    name: str
    error_code: int
    message: str
    exception: Exception

    def reply(self):
        '''Data to be sent from the server to the client through Flask.
        '''
        return self.message, self.error_code

    def raise_exception(self):
        '''Raise the exception on the client side.
        '''
        return self.exception(self.message)
    

error_list = [
    Error('key_not_provided', 460, werkzeug.exceptions.BadRequest, 'A key parameter must be provided when putting or accessing this resource.'),
    Error('repository_not_found', 461, KeyError, 'The requested repository was not found on the server.'),
    Error('key_not_found', 461, KeyError, 'The requested key was not found on the server.'),
    #Error('data_not_found', 404, werkzeug.exceptions.NotFound, 'The requested data was not found on the server.'),
]

errors = {e.name: e for e in error_list}













