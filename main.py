import webapp2
import re

#CODE FOR FORM
signup_form = """
<html>
    <head>
    <title>Signup</title>
    <style type="text/css">
    .error {color:red}
    </style>

        <body>
            <form method="post">
            <table>
                <tr>
                    <td class="label">
                        <b>Username:</b>
                    </td>
                    <td>
                        <input type="text" name="username">
                    </td>
                    <td class="error">
                        %(error_username)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        <b>Password:</br>
                    </td>
                    <td>
                        <input type="password" name="password">
                    </td>
                    <td class="error">
                        %(error_password)s
                    </td>
                </tr>

                <tr>
                    <td class="label"> <b>Re-Enter Password:<br>
                    </td>
                    <td>
                        <input type="password" name="verifypw">
                    </td>
                    <td class="error">
                        %(error_verify)s
                    </td>
                </tr>

                <tr>
                    <td class="label">
                        <b>Email</b> (optional)<b>:</b>
                    </td>
                    <td>
                        <input type="text" name="email">
                    </td>
                    <td class="error">
                        %(error_email)s
                    </td>
                </tr>
            </table>

            <input type="submit">
            </form>
        </body>

</html>
"""

#CODE FOR WELCOME PAGE
welcome_form = """
<html>
    <head><title>Welcome!</title></head>
        <body>
            Heck yeah <b>%(username)s!</b> You did it!
        </body>
</html>
"""

#TESTING FUNCTIONS
user_regex = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and user_regex.match(username)

pw_regex = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and pw_regex.match(password)

email_regex = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or email_regex.match(email)

#SIGNUP(VERIFICATION,REDIRECT TO WELCOME IF SUCCESSFUL)
class SignUp(webapp2.RequestHandler):

    def initial_form(self, username='username', error_username='', error_password='', error_verify='', email='email', error_email=''):
        self.response.write(signup_form % {'username': username,'error_username': error_username,'error_password': error_password,'error_verify': error_verify,'email': email,'error_email': error_email})

    def get(self):
        self.initial_form()

    def post(self):
        have_error = False
        username=self.request.get('username')
        password=self.request.get('password')
        verify=self.request.get('verifypw')
        email=self.request.get('email')
        error_username, error_email, error_password, error_verify = "", "", "", ""

        if not valid_username(username):
            have_error = True
            error_username = 'Error: That is an invalid username'

        if not valid_password(password):
            have_error = True
            error_password = 'Error: That is an invalid password'

        if verify != password:
            have_error = True
            error_verify = 'Error: The passwords do not match'

        if not valid_email(email):
            have_error = True
            error_email = 'Error: That is an invalid e-mail address'

        if have_error:
            self.response.write(signup_form % {'username': username,'error_username': error_username,'error_password': error_password,'error_verify': error_verify,'email': email,'error_email': error_email})
        else:
            self.redirect('/welcome?username=' + username)

#WELCOME PAGE W/ USERNAME
class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.response.write(welcome_form % {'username': username})

app = webapp2.WSGIApplication([('/', SignUp), ('/welcome', Welcome)], debug=True)
