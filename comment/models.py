from google.appengine.ext import db
import datetime
from people.models import User
from django import forms
from django.db import models
    
class Comment(db.Model):
    target = db.ReferenceProperty(db.Model, collection_name='Comments')
    content = db.TextProperty(required=True, )
    author = db.ReferenceProperty(User)
    
    # create time
    ctime = db.DateTimeProperty(auto_now_add=True)   
    #last update time
    mtime = db.DateTimeProperty(auto_now=True)    
    # language, for filtering and automatic translation support
    lang = db.StringProperty(required=True, default='en')
    
    @models.permalink
    def get_absolute_url(self):
        return ('comment.views.show_comment', [self.key()])    

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ('author', 'ctime', 'mtime', 'lang', 'target')          