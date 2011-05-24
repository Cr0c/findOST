(function($) {	
	$.fn.autoAddingTextFields = function(class) {
		var t = $(this);
		var add_field = function() {
			if ($(this).val() == '') return;
			
			objects = t.children('div.'+ class);
			
			// unbind last object and add focusout event
			objects.last().children('input[type=text]')
												.unbind('input');
												
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
								 .bind('input', add_field);
			// add remove link to previous last object
			objects.last().appendRemoveLink();
			// update objects
			objects = t.find('div.' + class);
		};
		var objects = t.find('div.' + class);
		objects.not(':last').appendRemoveLink();
														
		objects.last().children('input[type=text]')
											.bind('input', add_field);
		return t;
	}
	
	$.fn.appendRemoveLink = function() {
		return $(this).each(function() {
			div = $(this);
			$('<a href="#" class="confirm" style="display:none;">Cancel	</a>').click(function(){
				$(this).siblings('.remove').show();
				$(this).siblings('.confirm').hide();
				$(this).hide();
				return false;
			}).appendTo(div);
			$('<a href="#" class="confirm" style="display:none;">Confirm</a>').click(function(){
				$(this).removeObject();
				return false;
			}).appendTo(div);
			$('<a href="#" class="remove">×</a>').click(function(){
				$(this).hide();
				$(this).siblings('.confirm').show();
				return false;
			}).appendTo(div);
		});
	}
	
	$.fn.removeObject = function() {
		$(this).siblings('input').val('');
		$(this).parent().hide();
	}
})(jQuery);

