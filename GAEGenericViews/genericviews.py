
from django.http import HttpResponse, Http404
from django.core.paginator  import Paginator, InvalidPage
from renderhelpers.utils import AutoRendResponse

class GenericViews():

    @classmethod
    def object_list(cls, request, queryset = None):        
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
        object = cls.model.get_by_id(int(id))
        if object is None: 
            raise Http404('%s Not found.' % id) 
      
        return AutoRendResponse(request, template='article/article_detail.html', autoAjax=False, redirectBack=False, context=locals())
