

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', help='Port to listen on.')


    args = parser.parse_args()
    print(args)
    print(args.hello)

    #print('hello world', __name__)

