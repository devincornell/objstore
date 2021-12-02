
import pathlib
import pickle
import typing
import gc

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
            raise RepoDoesNotExist(repo_name)
            
        return repo
    
    def make_repo(self, repo_name: str):
        '''Make a new repository on the server.
        '''
        if repo_name in self.data.keys():
            raise RepoAlreadyExists(repo_name)
        
        self.data[repo_name] = {}

    def delete_repo(self, repo_name: str):
        '''Make a new repository on the server.
        '''
        try:
            del self.data[repo_name]
        except KeyError as e:
            raise RepoDoesNotExist(repo_name)
        
        # garbage collect
        gc.collect()

    def get_data(self, repo_name: str, key: str = None):
        '''Get the data from the given repository.
        '''
        repo = self.get_repo(repo_name)
        if key is None:
            return repo
        else:
            try:
                data = repo[key]
            except KeyError:
                raise KeyDoesNotExist(repo_name, key)
            
            return data

    def put_data(self, repo_name: str, key: str, newdata: typing.Any):
        '''Create data in the existing repository.
        '''
        repo = self.get_repo(repo_name)
        repo[key] = newdata

    def delete_data(self, repo_name: str, key: str):
        '''Make a new repository on the server.
        '''
        repo = self.get_repo(repo_name)
        try:
            del repo[key]
        except KeyError as e:
            raise KeyDoesNotExist(repo_name, key)
        
        # garbage collect
        gc.collect()
