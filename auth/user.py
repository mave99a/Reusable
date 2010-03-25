from google.appengine.api import users
from google.appengine.ext import db
from people.models import create_new_user_profile
from django.utils import simplejson

class AnonymousUser: 
    def is_authenticated(self):   
        return False
    
    def user(self):        
        return None
    
    def name(self):
        return 'Guest'
    
    def email(self):
        return '@'
            
class GoogleUser(db.Model):     
    user = db.ReferenceProperty(db.Model, required=True)
    googleuser = db.UserProperty(required=True)

        
    def is_authenticated(self):   
        return True
    
    @classmethod
    def login_html(cls):
        return '<a href="%s">Google User Signin</a>' % users.create_login_url("/")
    
    @classmethod
    def logout_html(cls):
        return '<a href="%s">Logout</a>' % users.create_logout_url("/")
    
    @classmethod
    def getUser(cls, request):
        googleuser = users.get_current_user() 
        if googleuser:
            result = GoogleUser.all().filter('googleuser =', googleuser).get()
            if result is None:
                newuser = create_new_user_profile(googleuser.nickname(), simplejson.dumps({'type':'gravatar', 'email': googleuser.email()}))
                result = GoogleUser(user=newuser, googleuser = googleuser)
                result.put()
            return result    
        else:
            return None
    
    def name(self):
        return self.googleuser.nickname()
    
    def email(self):
        return self.googleuser.email()
    
class FacebookUser(db.Model):
    user = db.ReferenceProperty(db.Model, required=True)
    fbuid = db.StringProperty(required=True)
        
    @classmethod
    def login_html(cls):
        return '<fb:login-button v="2" size="small" onlogin="window.location=returnURL">Login with Facebook</fb:login-button>'
 
    @classmethod
    def logout_html(cls):
        #return '<fb:login-button v="2" size="large" autologoutlink="true" onlogin="window.location=returnURL">Login with Facebook</fb:login-button>'
        return    '<fb:login-button size="small" background="white" length="long" autologoutlink="true"></fb:login-button>'
    @classmethod
    def getUser(cls, request):
        if getattr(request, 'facebook', None):
            fb = request.facebook
            if fb.check_session(request):                        
                result = FacebookUser.all().filter('fbuid =', fb.uid).get()
                if result is None:                  
                    newuser = create_new_user_profile(fb.uid, simplejson.dumps({'type':'facebook', 'fbuid': fb.uid}))
                    result = FacebookUser(user=newuser, fbuid = fb.uid)
                    result.put()
                return result   
        return None
        
    def is_authenticated(self):   
        return True

    def name(self):
        return self.fbuid
    
    def email(self):
        return self.fbuid
    
def get_current_user(request):
    AuthMethods = [FacebookUser, GoogleUser]
    for method in AuthMethods:
        user = method.getUser(request)
        if user:
            return user
    return AnonymousUser()    
