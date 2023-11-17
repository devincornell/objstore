import uvicorn
import argparse
from .server import run_server
from .client import Client

import typing
import click
import inspect

@click.group()#context_settings=CONTEXT_SETTINGS)
def greet():
    pass

@greet.command(help='Start the fastapi uvicorn server.')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default='8000', type=int)
@click.option('-l', '--loglevel', default='info')
#@click.option('--ignorecache', is_flag=True, default=False) # TODO
def server(**kwargs) -> None:
    return run_server(
        host=kwargs['host'], 
        port=kwargs['port'], 
        log_level=kwargs['loglevel'],
    )

import requests.exceptions

@greet.command(help='List the keys running in the server.')
@click.option('-h', '--host', default='localhost')
@click.option('-p', '--port', default='8000', type=int)
@click.option('--repo', default=None)
def list(**kwargs) -> None:
    try:
        client = Client(kwargs['host'], kwargs['port'])
    except requests.exceptions.ConnectionError as e:
        #print(e)
        print(f'Error: could not connect to server at {kwargs["host"]}:{kwargs["port"]}.')
        return
    
    if not client.status()['is_alive']:
        raise RuntimeError('Could not get status from server.')
    
    for rname in client.list_repos():
        print(f'  {rname}')
        repo = client.get_repo(rname)
        for k in repo.list_keys():
            print(f'    {k}')
    
    client.list_repos()
    
if __name__ == '__main__':
    greet()
    