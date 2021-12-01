
import pathlib
import pickle
import typing

from ..errors import KeyDoesNotExist, RepoDoesNotExist, RepoAlreadyExists

class RepoData:
    '''Represents the data stored on the server.
    '''
    def __init__(self, fname: str = None):
        self.fpath = pathlib.Path(fname) if fname is not None else None

        # load data or use empty
        if self.fpath is None:
            self.data = dict()
        else:
            with self.fpath.open('rb') as f:
                self.data = pickle.load(f)

    def __len__(self):
        return len(self.data)

    def num_items(self):
        return sum([len(v) for v in self.data.values()])

    def list_repos(self):
        return list(self.data.keys())

    def get_repo(self, repo_name: str):
        '''Get data from an existing repository.
        '''
        try:
            repo = self.data[repo_name]
        except KeyError:
            raise RepoDoesNotExist(f'The repository "{repo_name}" does not exist on the server.')
            
        return repo
    
    def set_repo(self, repo_name: str):
        '''Make a new repository on the server.
        '''
        if repo_name in self.data.keys():
            raise RepoAlreadyExists(f'The repository "{repo_name}" already exists'
                ' - cannot create it twice.')
        
        self.data[repo_name] = {}

    def get_data(self, repo_name: str, key: str):
        '''Get the data from the given repository.
        '''
        repo = self.get_repo(repo_name)
        try:
            data = repo[key]
        except KeyError:
            raise KeyDoesNotExist()
        
        return data

    def set_data(self, repo_name: str, key: str, newdata: typing.Any):
        '''Create data in the existing repository.
        '''
        repo = self.get_repo(repo_name)
        repo[key] = newdata

