
import pickle
import pathlib
import typing

from ..interfaces import RepoCollectionInterface
from ..errors import KeyDoesNotExist, RepoDoesNotExist, RepoAlreadyExists
from .serverrepo import ServerRepo

class ServerRepoCollection(RepoCollectionInterface):
    
    def __init__(self, fname: str = None):
        
        # use this to store repositories
        self.repos: typing.Dict[str, ServerRepo] = list()

        self.fpath = pathlib.Path(fname) if fname is not None else None

        # load data or use empty
        #if self.fpath is None:
        #    self.data = dict()
        #else:
        #    with self.fpath.open('rb') as f:
        #        self.data = pickle.load(f)

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


