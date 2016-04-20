import os
import sys
import BaseHTTPServer
import fnmatch
import traceback
import urlparse
import webbrowser

# This can be changed if you want to run the examples server on an alternate port.
PORT = 7000

# Add the stackpy directory to $PATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all of the examples
from src.users     import UserExamples
from src.questions import QuestionExamples

class ExamplesServer(BaseHTTPServer.BaseHTTPRequestHandler):
    
    _examples = {'users':     UserExamples,
                 'questions': QuestionExamples,}
    
    def send_reply(self, status_code, content, content_type='text/html'):
        self.send_response(status_code)
        self.send_header('Content-length', str(len(content)))
        self.send_header('Content-type', content_type)
        self.end_headers()
        self.wfile.write(content)
    
    def do_GET(self):
        try:
            if self.path == '/':
                self.do_index()
            else:
                # Parse the requested path
                url = urlparse.urlparse(self.path)
                # Split the path into two parts - the example name and the parameters
                path = url.path if url.path.endswith('/') else url.path + '/'
                (example, parameters) = path[1:].split('/', 1)
                # Make sure the example exists
                if not example in self._examples:
                    self.send_reply(404, '<h2>404 Not Found</h2><p>The page you have requested (<code>%s</code>) was not found on this server.</p>' % url.path)
                # Launch the example
                inst = self._examples[example]()
                (status, content) = inst.do_request(parameters, urlparse.parse_qs(url.query))
                self.send_reply(status, content)
        except Exception, e:
            self.send_reply(500, '<h2>500 Internal Server Error</h2><p>An exception has occurred:</p><pre>%s</pre>' % e)
    
    def do_index(self):
        example_list = '<ul>'
        for example in self._examples:
            example_list += '<li><a href="/%s/">%s</a></li>' % (example, self._examples[example].description,)
        example_list += '</ul>'
        self.send_reply(200, '<h2>Examples:</h2>%s' % example_list)

# Create the server
httpd = BaseHTTPServer.HTTPServer(('localhost', PORT), ExamplesServer)

# Now open the user's default web browser to our local server.
webbrowser.open('http://localhost:%d' % PORT)

# Run the server indefinitely
httpd.serve_forever()