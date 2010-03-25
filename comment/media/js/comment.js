$(document).ready(function() {
	$('form.comment').ajaxForm({
            resetForm: true,
			success: function(data) {
                newadd = $('.comments_list table').prepend(data)
                
                if (typeof(FB) != 'undefined') {
                    // make sure newly added FBML get displayed correctly
                    FB.XFBML.Host.parseDomElement(newadd.find('td.author').get(0));
                }
			}
		}
	)
})