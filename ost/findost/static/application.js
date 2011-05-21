(function($) {	
	$.fn.autoAddingTextFields = function(class) {
		var t = $(this);
		var add_field = function() {
			if ($(this).val() == '') return;
			
			objects = t.children('div.'+ class);
			
			// unbind last object and add focusout event
			objects.last().children('input[type=text]')
												.unbind('keydown');
												
			// duplicate last one and bind keypress
			objects.last().clone().appendTo(t)
								 .find('input')
								 .attr('name', function(i, val) {
										return val.replace(/(\d+)/, function(match, n) {
											return  (Number(n)+1);
										});
								 })
								 .attr('id', function(i, val) {
										return val.replace(/(\d+)/, function(match, n) {
											return (Number(n)+1);
										});
								 })
								 .val('')
								 .keydown(add_field)
			// add remove link to previous last object
			objects.last().appendRemoveLink();
			// update objects
			objects = t.find('div.' + class);
		};
		var objects = t.find('div.' + class);
		objects.not(':last').appendRemoveLink();
														
		objects.last().children('input[type=text]')
											.keydown(add_field);
		return t;
	}
	
	$.fn.appendRemoveLink = function() {
		return $(this).each(function() {
			div = $(this);
			$('<a href="#" class="remove">×</a>').click(function(){
				$(this).removeObject();
				return false;
			}).appendTo(div);
		});
	}
	
	$.fn.removeObject = function() {
		$(this).siblings('input').val('');
		$(this).parent().hide();
	}
})(jQuery);

$(document).ready(function() {
	$("#actors").autoAddingTextFields("actor");
	$("#songs").autoAddingTextFields("song");
});
