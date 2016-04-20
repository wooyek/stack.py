from example import Example
from stackpy import Site

class UserExamples(Example):
    
    title = 'User Example'
    description = 'Simple examples of fetching user information with the API.'
    
    def page_body(self, parameters, query_string):
        if 'id' in query_string:
            # Create an instance of the Stack Overflow site
            so = Site('stackoverflow')
            # Try to get the user with the ID
            users = so.users(query_string['id'])
            if len(users):
                return 'Your username is %s.' % users[0].display_name
            else:
                return 'Sorry, but the ID you specified was invalid.'
        else:
            return '<form>Enter a user ID on Stack Overflow: <input type="text" name="id" /> <input type="submit" /></form>'