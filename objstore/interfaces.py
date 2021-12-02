

class RepoCollectionInterface:
    '''Represents multiple repositories.
    '''
    def num_items(self):
        raise NotImplementedError()

    def list_repos(self):
        raise NotImplementedError()

    def get_repo(self, repo_name: str):
        '''Get data from an existing repository.
        '''
        raise NotImplementedError()
    
    def make_repo(self, repo_name: str):
        '''Make a new repository on the server.
        '''
        raise NotImplementedError()

    def delete_repo(self, repo_name: str):
        '''Delete a repository from the server.
        '''
        raise NotImplementedError()


class RepoInterface:
    '''Represents a single repository in the data model.
    '''
    
    @property
    def name(self):
        raise NotImplementedError()

    def list_keys(self, repo_name: str):
        '''Get the data specified in the given repository.
        '''
        raise NotImplementedError()

    def get_all(self, repo_name: str):
        '''Get all data associated with the server.
        '''
        raise NotImplementedError()
    
    def get_data(self, repo_name: str, key: str = None):
        '''Get the data specified from the given repository.
        '''
        raise NotImplementedError()

    def put_data(self, repo_name: str, key: str, newdata: typing.Any):
        '''Create data in the existing repository.
        '''
        raise NotImplementedError()

    def delete_data(self, repo_name: str, key: str):
        '''Make a new repository on the server.
        '''
        raise NotImplementedError()
