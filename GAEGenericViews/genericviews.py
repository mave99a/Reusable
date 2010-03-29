from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.core.paginator  import Paginator, InvalidPage
from renderhelpers.utils import AutoRendResponse

class GenericViews():

    @classmethod
    def get_object_or_404(cls, id):
        try:
            if type(id) is not int:
                id = int(id)
                
            if cls.model is not None: 
                object = cls.model.get_by_id(id)
                if object is None: 
                    raise Http404('%s Not found.' % id)
                else :
                    return object
            else:
                raise Http404('Model is not defined in Generic View.')
        except: 
            raise Http404('Not found')
        
    @classmethod
    def list(cls, request, queryset = None):        
        paginator = Paginator(queryset, 3,  allow_empty_first_page=True)
        page = request.GET.get('page', 1)
            
        try:
            page_number = int(page)
        except ValueError:
            if page == 'last':
                page_number = paginator.num_pages
            else:
                # Page is not 'last', nor can it be converted to an int.
                page_number = 1
        try:
            page_obj = paginator.page(page_number)
        except InvalidPage:
            page_obj = paginator.page(1)
    
        object_list = page_obj.object_list
        
        return AutoRendResponse(request, template='article/article_list.html', autoAjax=False, redirectBack=False, context=locals())


    @classmethod
    def detail(cls, request, id, title=None):
        object = cls.get_object_or_404(id)      
        return AutoRendResponse(request, template='article/article_detail.html', autoAjax=False, redirectBack=False, context=locals())

    @classmethod
    def create(cls):
        pass
    
    @classmethod
    def update(cls, request, id):
        object = cls.get_object_or_404(id)  
        if request.method  == 'POST':
            return cls.update_POST(request, object)
        else: 
            return cls.update_GET(request, object)     
        
    @classmethod
    def update_GET(cls, request, object):
        return AutoRendResponse(request, template='article/edit.html', autoAjax=False, redirectBack=False, context={'object':object})      

    @classmethod
    def update_POST(cls, request, object):
        form = cls.form(request.POST, request.FILES, instance=object)
        if form.is_valid():    
            new_object = form.save(commit = False)  
            new_object.put()
            return HttpResponseRedirect('/article/')
        
    @classmethod
    def delete(cls, request, id):
        object = cls.get_object_or_404(id)   
                
        if request.method  == 'POST':
            return cls.delete_POST(request, object)
        else: 
            return cls.delete_GET(request, object)
        
    @classmethod
    def delete_GET(cls, request, object):
        return AutoRendResponse(request, template='article/article_confirm_delete.html', autoAjax=False, redirectBack=False, context={'object':object})      
    
    @classmethod
    def delete_POST(cls, request, object):
        object.delete()
        return HttpResponseRedirect('/article/')