import json
from urllib.parse import parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer

credentials = {
    'Cyberman': 'John Lumic',
    'Dalek': 'Davros',
    'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
    'Human': 'Leonardo da Vinci',
    'Ood': 'Klineman Halpen',
    'Silence': 'Tasha Lem',
    'Slitheen': 'Coca-Cola salesman',
    'Sontaran': 'General Staal',
    'Time Lord': 'Rassilon',
    'Weeping Angel': 'The Division Representative',
    'Zygon': 'Broton',
    'Mage': 'Anthonidas'
}


def wsgi_app(environ, start_response):
    status = '200 OK'

    query_string = environ.get('QUERY_STRING', '')
    params = parse_qs(query_string)

    species = params.get('species', [None])[0]
    if species and species in credentials:
        response_data = {'credentials': credentials[species]}
        status = '200 OK'
    else:
        response_data = {'credentials': 'Unknown'}
        status = '404 Not Found'

    headers = [('Content-Type', 'application/json')]
    start_response(status, headers)
    return json.dumps(response_data).encode('utf-8')


class WSGIRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        environ = {
            'REQUEST_METHOD': 'GET',
            'PATH_INFO': self.path,
            'QUERY_STRING': self.path.split('?', 1)[1] if '?' in self.path else '',
            'SERVER_NAME': self.server.server_name,
            'SERVER_PORT': str(self.server.server_port),
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': self.rfile,
            'wsgi.errors': self.wfile,
            'wsgi.multithread': False,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
        }

        def start_response(status, headers):
            self.send_response(int(status.split()[0]))
            for header in headers:
                self.send_header(header[0], header[1])
            self.end_headers()

        response_body = wsgi_app(environ, start_response)

        self.wfile.write(response_body)


def run(server_class=HTTPServer, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, WSGIRequestHandler)
    # print(f'Serving on port {port}...')
    httpd.serve_forever()


if __name__ == '__main__':
    run()
