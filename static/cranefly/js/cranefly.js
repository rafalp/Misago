$(function () {
	// Register tooltips
	$('.tooltip-top').tooltip({placement: 'top', container: 'body'})
	$('.tooltip-bottom').tooltip({placement: 'bottom', container: 'body'})
	$('.tooltip-left').tooltip({placement: 'left', container: 'body'})
	$('.tooltip-right').tooltip({placement: 'right', container: 'body'})
	
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
    $(this).wrap(function() { return '<div class="md-img" />'; });
    $(this).wrap(function() { return '<div class="span5 md-img-span" />'; });
    $(this).wrap(function() { return '<div class="md-img-wrap" />'; });
    $(this).after('<a href="' + $(this).attr('src') + '" class="md-img-label" target="_blank">' + $(this).attr('alt') + '</a>');
    $(this).wrap(function() { return '<div class="md-img-bg" />'; });
	});

	// Handle prokened images
  $('.markdown img').one('error', function() {
  	$(this).after('<div class="md-img-error"><span>' + l_img_broken_msg + '</span></div>');
  	$(this).hide();
	});
	
	// Automagically turn links into players
	$('.markdown a').each(function() {
		// Youtube link
		var re = /watch\?v=([A-Za-z0-9]+)/;
		if (re.test(this.href)) {
			media_url = this.href.match(re);
			$(this).replaceWith('<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>');
			return;
		}

		// Youtube embed with start time
		var re = /youtu.be\/([A-Za-z0-9]+)\?t=([A-Za-z0-9]+)/;
		if (re.test(this.href)) {
			media_url = this.href.match(re);
			media_minutes = media_url[2].match(/([0-9]+)m/);
			media_seconds = media_url[2].match(/([0-9]+)s/);
			media_url[2] = 0;
			if (media_minutes) { media_url[2] += (media_minutes[1] - 0) * 60; }
			if (media_seconds) { media_url[2] += (media_seconds[1] - 0); }
			$(this).replaceWith('<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '?start=' + media_url[2] + '" frameborder="0" allowfullscreen></iframe>');
			return;
		}
		
		// Youtube embed
		var re = /youtu.be\/([A-Za-z0-9]+)/;
		if (re.test(this.href)) {
			media_url = this.href.match(re);
			$(this).replaceWith('<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>');
			return;
		}

		// Vimeo link
		var re = /vimeo.com\/([0-9]+)/;
		if (re.test(this.href)) {
			media_url = this.href.match(re);
			$(this).replaceWith('<iframe src="http://player.vimeo.com/video/' + media_url[1] + '?color=CF402E" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>');
			return;
		}
	});
})