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

  // Fancy user nav activation
  $('#fancy-user-nav').show();

  // Search form extension
  var nav_search_form = $('#navbar-search');
  $('#search-field').hover(function() {
    nav_search_form.addClass('open');
  });

  $('html').click(function() {
    nav_search_form.removeClass('open');
  });

  nav_search_form.click(function(event) {
    event.stopPropagation();
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
    $('.markdown.js-extra img').not('.emoji').each(function() {
      $(this).addClass('img-rounded');
      if ($(this).attr('alt').length > 0 && $(this).attr('alt') != $(this).attr('src')) {
        $(this).attr('title', $(this).attr('alt'));
        $(this).tooltip({placement: 'top', container: 'body'});
      }
    });

    // Automagically turn links into players
    var players = new Array();
    $('.markdown.js-extra').each(function() {
      var post_players = 0;
      $(this).find('a').each(function() {
        match = link2player($.trim($(this).text()));
        if (match && $.inArray(match, players) == -1 && players.length < 16 && post_players < 4) {
          players.push(match);
          post_players ++;
          $(this).replaceWith(match);
        }
      });
    });
  });
}

// Turn link to player
function link2player(link_href) {
  // Youtube link
  var re = /watch\?v=((\w|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>';
  }

  // Youtube feature=embed
  var re = /watch\?feature=player_embedded&v=((\w|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>';
  }

  // Youtube embed with start time
  var re = /youtu.be\/((\w|-)+)\?t=([A-Za-z0-9]+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    media_minutes = media_url[2].match(/([0-9]+)m/);
    media_seconds = media_url[2].match(/([0-9]+)s/);
    media_url[2] = 0;
    if (media_minutes) { media_url[2] += (media_minutes[1] - 0) * 60; }
    if (media_seconds) { media_url[2] += (media_seconds[1] - 0); }
    return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '?start=' + media_url[2] + '" frameborder="0" allowfullscreen></iframe>';
  }
  
  // Youtube embed
  var re = /youtu.be\/((\w|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return '<iframe width="480" height="360" src="http://www.youtube.com/embed/' + media_url[1] + '" frameborder="0" allowfullscreen></iframe>';
  }

  // Vimeo link
  var re = /vimeo.com\/([0-9]+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return '<iframe src="http://player.vimeo.com/video/' + media_url[1] + '?color=CF402E" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>';
  }

  // No link
  return false;
}

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
      }).fail(function() {
        $(form).unbind();
        $(form).trigger('submit');
      });
      return false;
    });
  });
});

// Ajax: Post reports
$(function() {
  $('.form-report').each(function() {
    var action_parent = this;
    var csrf_token = $(this).find('input[name="_csrf_token"]').val();
    var button = $(this).find('button');
    $(this).submit(function() {
      var form = this;
      $.post(form.action, {'_csrf_token': csrf_token}, "json").done(function(data, textStatus, jqXHR) {        
        $(button).text(l_post_reported);
        $(button).tooltip('destroy');
        $(button).attr("title", data.message);
        $(button).tooltip({placement: 'top', container: 'body'});
        $(button).tooltip("show");
        $(button).attr("disabled", "disabled");
        setTimeout(function() {
          $(button).tooltip('hide');
        }, 2500);
      }).fail(function() {
        $(form).unbind();
        $(form).trigger('submit');
      });
      return false;
    });
  });
});