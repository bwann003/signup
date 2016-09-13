import webapp2
import re

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Index(webapp2.RequestHandler):
    form = """
    <form method="post">
        <label>
            Username:
            <input type="text" name="username"/>
        </label>
        <br><br>
        <label>
            Password:
            <input type="password" name="password" value=""/>
        </label>
        <br><br>
        <label>
            Verify Password:
            <input type="password" name="verify" value=""/>
        </label>
        <br><br>
        <label>
            Email Address (optional)
            <input type="text" name="email" value="example@email.com"/>
        </label>
        <br><br>
        <label>
            <input type="submit" value="submit"/>
        </label>
    </form>

    """

    def get(self):
        #display form
        self.response.out.write(self.form)

    def post(self):
        have_error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)

        if not valid_username(username):
            params['error_username'] = "That's not a valid username."
            have_error = True

        if not valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            have_error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            have_error = True

        if not valid_email(email):
            params['error_email'] = "That's not a valid email."
            have_error = True

        if have_error:
            self.render('/', **params)
        else:
            self.redirect('/welcome?username=' + username)


class Welcome(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome <b>" + username + "</b>!")


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/welcome', Welcome)
], debug=True)


#USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
#def valid_username(username):
#return USER_RE.match(username)
