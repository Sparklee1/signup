#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

form="""
<form method = "post">
    <h1>Signup</h1>
    <br>
    <label>
        Username
        <input type = "text", name = "username", value = "%(username)s"/>
        <div style = "color: red">%(userError)s</div>
    </label>
    <br>
    <br>
    <label>
        Password
        <input type = "password", name = "password", value = ""/>
        <div style = "color: red">%(passError)s</div>
    </label>
    <br>
    <br>
    <label>
        Verify Password
        <input type = "password", name = "verify", value = ""/>
        <div style = "color: red">%(verifyError)s</div>
    </label>
    <br>
    <br>
    <label>
        Email (optional)
        <input type = "text", name = "email", value = "%(email)s"/>
    </label>
    <br>
    <br>
    <input type = "submit"/>
</form>
"""

import webapp2
import re
import cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return not email or USER_EMAIL.match(email)

def escape (s):
    return cgi.escape(s, quote=True)

class MainHandler(webapp2.RequestHandler):

    def display_form(self, username = "", userError = "", password = "", passError = "", verify = "", verifyError = "", email = "", emailError = ""):
        self.response.write(form % {"username":escape(username),
                                    "userError": userError,
                                    "passError": passError,
                                    "verifyError": verifyError,
                                    "email":escape(email),
                                    "emailError": emailError, })

    def get(self):
        self.display_form()

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        userError = ""
        passError = ""
        verifyError = ""
        emailError = ""

        if not valid_username(username):
            error = True
            userError = "That is an invalid Username"


        if not valid_password(password):
            error = True
            passError = "That is an invalid Password"


        if not password == verify:
            error = True
            verifyError = "Your passwords do not match"

        if not valid_email(email):
            error = True
            emailError = "Your email is invalid"

        if error:
            self.display_form(username, userError, passError, verifyError, email, emailError)
        else:
            self.redirect("/thanks?username="+username)


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        self.response.out.write("Welcome, {0}" .format(username))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)
