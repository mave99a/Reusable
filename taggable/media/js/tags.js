/*
*  Initialize
*/
function attach_tags_handlers()
{
  	$('a.tag span.remove').click(function() {
  				$(this).parent().addClass('deletedtag').removeClass('tag').blur();
  				$.get($(this).attr('href'));
				return false; // cancel event 
	})
   	$('a.tag span.undo').click(function() {
  				$(this).parent().addClass('tag').removeClass('deletedtag').blur();
  				$.get($(this).attr('href'));
				return false; // cancel event 
	}) 	
}

$(document).ready(function() {
  if (typeof(_JS_MODULE_TAG) != 'undefined') {
	
	attach_tags_handlers()
	
	$('.tags form').ajaxForm({
            resetForm: true,
            dataType: 'json',
			success: function(data) {
								if (data.success) {
									$('span.tagscontainer').html(data.html)
									attach_tags_handlers()
								}
								else {
									// error 
								}
					}
		}
	)		   
  }
});

