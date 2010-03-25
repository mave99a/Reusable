# -*- coding: utf-8 -*-
from google.appengine.ext import db
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic.list_detail import object_list, object_detail
from django.http import HttpResponse, HttpResponseRedirect
from auth.decorators import login_required
from renderhelpers.renderblock import render_block_to_string
from renderhelpers.decorators import AutoResponse

from models import *
from sys import maxint

@AutoResponse(template='taggable/tag_list.html', autoAjax=False, redirectBack=False)
def tagcloud(request):
    object_list = Tag.cloud(100).fetch(100)
    min = 1
    max = maxint
    
    # find out the max and min of the tag count
    for item in object_list:
        if item.count > max:
            max = item.count 
        if item.count < min:
            min = item.count
    
    step = (max - min)/6
    # calculate the size
    for item in object_list:
        item.cloudsize = (item.count - min) % step
        
    return locals()
    
def show_by_tag(request, tag):
    return object_list(request, Taggable.get_by_tag(tag), paginate_by = 10, 
                       extra_context={'tag':tag})

@login_required
@AutoResponse(autoAjax=True, redirectBack=True)
def add_tags(request):
    key = request.REQUEST["target"]
    tags = request.REQUEST["tags"].split(',')
    obj = db.get(key)
    taggable = Taggable.add_tags(obj, tags)
    if taggable is not None:
        return taggable.tags
    else:
        return []

@login_required
@AutoResponse(autoAjax=True, redirectBack=True)
def add_tags_form(request):
    key = request.REQUEST["target"]
    tags = request.REQUEST["tags"].split(',')
    obj = db.get(key)
    taggable = Taggable.add_tags(obj, tags)
    
    if request.is_ajax(): 
        result = render_block_to_string('taggable/tags.html', 'tags', {'taggable': taggable, 'editable': True})
        return {'success': True, 'html': result}

 
@login_required
@AutoResponse(autoAjax=True, redirectBack=True)
def remove_tags(request):
    key = request.REQUEST["target"]
    tags = request.REQUEST["tags"].split(',')
    obj = db.get(key)
    taggable = Taggable.remove_tags(obj, tags)
    if taggable is not None:
        return taggable.tags
    else:
        return []


@login_required
def my_tags(request):
   return  HttpResponse('ok')