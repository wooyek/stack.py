# Base class that provides common functionality for examples
class Example:
    
    def do_request(self, parameters, query_string):
        return (200, '''<!DOCTYPE html>
<html>
<head>
  <title>%s</title>
  <style>
    
    body {
        font-family: arial, helvetica, sans;
    }
    
  </style>
</head>
<body>
%s
</body>
</html>''' % (self.title, self.page_body(parameters, query_string),))