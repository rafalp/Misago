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

	// Dont fire popovers on touch devices
	$("[class^='tooltip-']").on('show', function (e) {
	  if ('ontouchstart' in document.documentElement) {
	  	e.preventDefault();
	  }
	});
	
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
	
	// Show go back link?
	if (document.referrer
			&& document.referrer.indexOf(location.protocol + "//" + location.host) === 0
			&& document.referrer != document.url) {
		$('.go-back').show();
	}

	// Go back one page
	$('.go-back').on('click', function (e) {
	    history.go(-1)
	    return false;
	})
})

function EnhancePostsMD() {
	$(function () {
		// Add labels to images
		$('.markdown.js-extra img').each(function() {
	    $(this).addClass('img-rounded');
	    $(this).wrap(function() { return '<div class="md-img" />'; });
	    $(this).wrap(function() { return '<div class="span5 md-img-span" />'; });
	    $(this).wrap(function() { return '<div class="md-img-wrap" />'; });
	    $(this).after('<a href="' + $(this).attr('src') + '" class="md-img-label" target="_blank">' + $(this).attr('alt') + '</a>');
	    $(this).wrap(function() { return '<div class="md-img-bg" />'; });
		});

		// Handle prokened images
	  $('.markdown.js-extra img').one('error', function() {
	  	$(this).after('<div class="md-img-error"><span>' + l_img_broken_msg + '</span></div>');
	  	$(this).hide();
		});

		// Automagically turn links into players
		var players = new Array();
		$('.markdown.js-extra a').each(function() {
			if (this.href == $.trim($(this).text())) {
				match = link2player(this);
				if (match && $.inArray(match, players) == -1) {
					players.push(match);
					$(this).replaceWith(match);
					if (players.length == 10) {
						return false;
					}
				}
			}
		});
	});
}

// Turn link to player
function link2player(link) {
	// Youtube link
	var re = /watch\?v=((\w|-)+)/;
	if (re.test(link.href)) {
		media_url = link.href.match(re);
		return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>';
	}

	// Youtube embed with start time
	var re = /youtu.be\/((\w|-)+)\?t=([A-Za-z0-9]+)/;
	if (re.test(link.href)) {
		media_url = link.href.match(re);
		media_minutes = media_url[2].match(/([0-9]+)m/);
		media_seconds = media_url[2].match(/([0-9]+)s/);
		media_url[2] = 0;
		if (media_minutes) { media_url[2] += (media_minutes[1] - 0) * 60; }
		if (media_seconds) { media_url[2] += (media_seconds[1] - 0); }
		return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '?start=' + media_url[2] + '" frameborder="0" allowfullscreen></iframe>';
	}
	
	// Youtube embed
	var re = /youtu.be\/((\w|-)+)/;
	if (re.test(link.href)) {
		media_url = link.href.match(re);
		return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>';
	}

	// Vimeo link
	var re = /vimeo.com\/([0-9]+)/;
	if (re.test(link.href)) {
		media_url = link.href.match(re);
		return '<iframe src="http://player.vimeo.com/video/' + media_url[1] + '?color=CF402E" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';
	}

	// No link
	return false;
}

// Ajax errors handler
$(document).ajaxError(function(event, jqXHR, settings) {
	var responseJSON = jQuery.parseJSON(jqXHR.responseText);
	if (responseJSON.message) {
		alert(responseJSON.message);
	}
});

// Ajax: Post votes
$(function() {
	$('.post-rating-actions').each(function() {
		var action_parent = this;
		var csrf_token = $(this).find('input[name="_csrf_token"]').val();
		$(this).find('form').submit(function() {
			var form = this;
			$.post(this.action, {'_csrf_token': csrf_token}, "json").done(function(data, textStatus, jqXHR) {
				// Reset stuff and set classess
				$(action_parent).find('.post-score').removeClass('post-score-good post-score-bad');
				if (data.score_total > 0) {
					$(action_parent).find('.post-score-total').addClass('post-score-good');
				} else if (data.score_total < 0) {
					$(action_parent).find('.post-score-total').addClass('post-score-bad');
				} 
				if (data.score_upvotes > 0) {
					$(action_parent).find('.post-score-upvotes').addClass('post-score-good');
				}
				if (data.score_downvotes > 0) {
					$(action_parent).find('.post-score-downvotes').addClass('post-score-bad');
				}

				// Set votes
				$(action_parent).find('.post-score-total').text(data.score_total);
				$(action_parent).find('.post-score-upvotes').text(data.score_upvotes);
				$(action_parent).find('.post-score-downvotes').text(data.score_downvotes);

				// Disable and enable forms
				if (data.user_vote == 1) {
					$(action_parent).find('.form-upvote button').attr("disabled", "disabled");
					$(action_parent).find('.form-downvote button').removeAttr("disabled");
				} else {
					$(action_parent).find('.form-upvote button').removeAttr("disabled");
					$(action_parent).find('.form-downvote button').attr("disabled", "disabled");
				}
			}).error();
			return false;
		});
	});
});
