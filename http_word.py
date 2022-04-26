from wsgiref.simple_server import make_server
 
import json
import spcy_test
 
 
def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/html')])
    query = environ.get('QUERY_STRING')
    print('query:{}'.format(query))
    print(query)
    print()
    spcy_test.main()
    return ['Hello, World'.encode('utf-8')]

with make_server('', 8000, application) as httpd:
    httpd.serve_forever()