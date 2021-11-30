
import pathlib
import pickle


from ..errors import KeyDoesNotExist, RepoDoesNotExist

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
    
    def __getitem__(self, repo_name: str):
        try:
            repo = self.data[repo_name]
        except KeyError:
            raise RepoDoesNotExist()
            
        return repo

    def __len__(self):
        return len(self.data)

    def num_items(self):
        return sum([len(v) for v in self.data.values()])

    def list_repos(self):
        return list(self.data.keys())

    def get_data(self, repo_name: str, key: str):
        repo = self[repo_name]
        try:
            data = repo[key]
        except KeyError:
            raise KeyDoesNotExist()
        
        return data
