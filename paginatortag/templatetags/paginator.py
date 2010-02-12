#
#  refer: http://blog.localkinegrinds.com/2007/09/06/digg-style-pagination-in-django/
#  styles: http://mis-algoritmos.com/2007/03/16/some-styles-for-your-pagination/
#
#  has been modified to use the "page_obj" and "paginator" only from context
#
from django import template
 
register = template.Library()
 
LEADING_PAGE_RANGE_DISPLAYED = TRAILING_PAGE_RANGE_DISPLAYED = 10
LEADING_PAGE_RANGE = TRAILING_PAGE_RANGE = 8
NUM_PAGES_OUTSIDE_RANGE = 2 
ADJACENT_PAGES = 4
 
def paginator(context):
    page_obj = context["page_obj"]
    paginator = context["paginator"]
    if (page_obj.has_other_pages()):
        " Initialize variables "
        page = page_obj.number
        pages =  paginator.num_pages
        in_leading_range = in_trailing_range = False
        pages_outside_leading_range = pages_outside_trailing_range = range(0)
 
        if (pages <= LEADING_PAGE_RANGE_DISPLAYED):
            in_leading_range = in_trailing_range = True
            page_numbers = [n for n in range(1, pages + 1) if n > 0 and n <= pages]           
        elif (page <= LEADING_PAGE_RANGE):
            in_leading_range = True
            page_numbers = [n for n in range(1, LEADING_PAGE_RANGE_DISPLAYED + 1) if n > 0 and n <= pages]
            pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
        elif (page > pages - TRAILING_PAGE_RANGE):
            in_trailing_range = True
            page_numbers = [n for n in range(pages - TRAILING_PAGE_RANGE_DISPLAYED + 1, pages + 1) if n > 0 and n <= pages]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        else: 
            page_numbers = [n for n in range(page - ADJACENT_PAGES, page + ADJACENT_PAGES + 1) if n > 0 and n <= pages]
            pages_outside_leading_range = [n + pages for n in range(0, -NUM_PAGES_OUTSIDE_RANGE, -1)]
            pages_outside_trailing_range = [n + 1 for n in range(0, NUM_PAGES_OUTSIDE_RANGE)]
        return {
            "is_paginated": page_obj.has_other_pages(),
            "previous": page_obj.previous_page_number(),
            "has_previous": page_obj.has_previous(),
            "next":  page_obj.next_page_number(),
            "has_next":  page_obj.has_next(),
            "results_per_page": paginator.per_page,
            "page": page,
            "pages": pages,
            "page_numbers": page_numbers,
            "in_leading_range" : in_leading_range,
            "in_trailing_range" : in_trailing_range,
            "pages_outside_leading_range": pages_outside_leading_range,
            "pages_outside_trailing_range": pages_outside_trailing_range
        }
 
register.inclusion_tag("paginator.html", takes_context=True)(paginator)