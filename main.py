
import objstore

if __name__ == '__main__':
    client = objstore.Client('localhost', port=8000)
    #print(client.host)
    print(client.list_repos())
    print(client.status())
    
    #user_repo = client.get_repo('userdata')
    #print(user_repo.get_keys())
    #print(user_repo.get_data('users'))
    #print(user_repo.get_all())
    #user_repo.put_data('friends', 'list of my friends')
    #print(user_repo.get_keys())
    #print(user_repo.get_data('friends'))

    #other_repo = client.get_repo('others')
    #other_repo.get_data()
    #res = requests.get('http://localhost:9999/hello?stop=5')
    #print(client.request('range', params={'stop':5}).json())
    
    #print(client.request('data', 'GET', params={'key':'duh'}))
    #print(client.request('hello', 'PUT'))
    #print(client.request('hello', 'POST'))
    #print(client.request('hello', 'GET'))
    
    
    
    #print(client.get_data('namez'))
    #print(client.put_data('age', 4))


