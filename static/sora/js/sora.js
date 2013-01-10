$(function () {
	// Register tooltips
	$('.tooltip-top').tooltip({placement: 'top'})
	$('.tooltip-bottom').tooltip({placement: 'bottom'})
	$('.tooltip-left').tooltip({placement: 'left'})
	$('.tooltip-right').tooltip({placement: 'right'})
	
	// Register popovers
	$('.popover-top').popover({placement: 'top'})
	$('.popover-bottom').popover({placement: 'bottom'})
	$('.popover-left').popover({placement: 'left'})
	$('.popover-right').popover({placement: 'right'})
	
	// Start all dropdowns
	$('.dropdown-toggle').dropdown()
	
	// Dont hide clickable dropdowns
	$('.dropdown-clickable').on('click', function (e) {
	  e.stopPropagation()
	});
	
	// Checkbox Group Master
	$('input.checkbox-master').live('click', function(){
		if($(this).is(':checked')){
			$('input.checkbox-member').attr("checked" ,"checked");
		}
		else
		{
			$('input.checkbox-member').removeAttr('checked');
		}
	});
	
	// Checkbox Group Member
	$('input.checkbox-member').live('click', function(){
		if(!$(this).is(':checked')){
			$('input.checkbox-master').removeAttr('checked');
		}
	});
	
	// Check Confirmation on links
	$('a.confirm').live('click', function(){
		var decision = confirm(jQuery.data(this, 'jsconfirm'));
		return decision
	});
	
	// Check Confirmation on forms
	$('form.confirm').live('submit', function(){
		data = $(this).data();
		var decision = confirm(data.jsconfirm);
		return decision
	});
	
	// Go back one page
	$('.go-back').on('click', function (e) {
	  history.go(-1)
	})
	
	// Add labels to images
	$('.markdown img').each(function() {
        $(this).addClass('img-rounded');
        $(this).wrap(function() {
            return '<div class="md-img span5" />';
        });
        $(this).after('<a href="' + $(this).attr('src') + '" class="md-img-label"><i class="icon-picture"></i> ' + $(this).attr('alt') + '</a>');
	});
})