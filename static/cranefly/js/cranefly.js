$(function () {
  // Register tooltips
  $('body').tooltip({placement: 'top', container: 'body', selector: '.tooltip-top'})
  $('body').tooltip({placement: 'bottom', container: 'body', selector: '.tooltip-bottom'})
  $('body').tooltip({placement: 'left', container: 'body', selector: '.tooltip-left'})
  $('body').tooltip({placement: 'right', container: 'body', selector: '.tooltip-right'})

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
  nav_search_form.click(function() {
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
      $(this).find('a').each(function() {
        link2player(this, $.trim($(this).text()));
      });
    });
  });
}

// Turn link to player
function link2player(element, link_href) {
  // Youtube link
  var re = /watch\?v=((\w|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return youtube_player(element, media_url[1]);
  }

  // Youtube feature=embed
  var re = /watch\?feature=player_embedded&v=((\w|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return youtube_player(element, media_url[1]);
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
    return youtube_player(element, media_url[1], media_url[2]);
  }

  // Youtube embed
  var re = /youtu.be\/(([A-Za-z0-9]|_|-)+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return youtube_player(element, media_url[1]);
  }

  // Vimeo link
  var re = /vimeo.com\/([0-9]+)/;
  if (re.test(link_href)) {
    media_url = link_href.match(re);
    return $(element).replaceWith('<iframe src="http://player.vimeo.com/video/' + media_url[1] + '?color=CF402E" width="500" height="281" frameborder="0" webkitAllowFullScreen mozallowfullscreen allowFullScreen></iframe>');
  }

  // No link
  return false;
}

// Youtube player
function youtube_player(element, movie_id, startfrom) {
  if (typeof startfrom != 'undefined') {
    player_url = 'http://www.youtube.com/embed/' + movie_id + '?start=' + startfrom + '&amp;autoplay=1';
  } else {
    player_url = 'http://www.youtube.com/embed/' + movie_id + '?autoplay=1';
  }

  // Replace link with fancy image
  var media_element = $('<div><div class="media-border youtube-player" data-movieid="' + movie_id + '"><div class="media-thumbnail" style="background-image: url(\'http://img.youtube.com/vi/' + movie_id + '/0.jpg\');"><a href="' + $.trim($(element).text()) + '" class="play-link" data-playerurl="' + player_url + '"><i class="icon-youtube-sign"></i><strong>' + l_play_media_msg + '</strong></a></div></div></div>');
  $(media_element).find('.play-link').click(function() {
    $(this).parent().replaceWith('<iframe width="853" height="480" src="' + $(this).data('playerurl') + '" frameborder="0" allowfullscreen></iframe>');
    return false;
  });
  $(element).replaceWith(media_element);
  // Fetch title, author name and thumbnail
  $.getJSON("https://gdata.youtube.com/feeds/api/videos/" + movie_id + "?v=2&alt=json",
            function(data, textStatus, jqXHR) {
              // Movie details
              var movie_title = data.entry.title.$t;
              var movie_author = data.entry.author['0'].name.$t
              $(media_element).find('.play-link').addClass('movie-title');
              $(media_element).find('.play-link strong').text(movie_title);
              $(media_element).find('.play-link').append(l_play_media_author.replace('{author}', movie_author));
              // Movie thumbnail
              var thumb = {height: 90, url: 'http://img.youtube.com/vi/' + movie_id + '/0.jpg'};
              console.log(data.entry['media$group']['media$thumbnail']);
              $(data.entry['media$group']['media$thumbnail']).each(function(key, yt_image) {
                if (thumb.height < yt_image.height) {
                  thumb = yt_image;
                }
              });
              $(media_element).find('.media-thumbnail').css('background-image', "url('" + thumb.url + "')");
            });
  return true;
}

// Ajax: Reports and Alerts
$(function() {
  var midman = $('.midman');
  var animation_speed = 0;
  var midman_arrow = midman.find('.midman-arrow');
  var midman_error = midman.find('.ajax-error');
  var midman_content = midman.find('.loaded-content');
  var midman_content_id = false;
  var midman_cache = new Array();
  var midman_request = false;

  function midman_open(content_id) {
    midman_error.hide();

    if (midman_content_id != false) {
      midman_close();
      if (midman_request != false) {
        midman_request.abort();
      }
    }

    midman_content_id = content_id;
    $(midman_content_id).parent().addClass('active');

    var button_offset = $(midman_content_id).parent().offset();
    $(midman_arrow).css('left', button_offset.left + ($(midman_content_id).parent().width() / 2) - 10);

    if (midman_content_id in midman_cache) {
      midman_content.html(midman_cache[midman_content_id]);
      midman.show(animation_speed);
      return;
    }

    midman_request = $.ajax({
      url: $(midman_content_id).attr('href')
    }).done(function(data) {
      midman_cache[midman_content_id] = data.html;
      midman_content.html(data.html);
      midman.show(animation_speed);
    });
  }

  function midman_close() {
    if (midman_content_id != false) {
      $(midman_content_id).parent().removeClass('active');
      midman_content_id = false;
      midman.hide(animation_speed);
    }
  }

  $('.midman-close').live('click', function() {
    midman_close()
  });

  $('.midman form').live('submit', function() {
    var csrf_token = $(this).find('input[name="_csrf_token"]').val();
    $.post(this.action, {'_csrf_token': csrf_token}, "json").done(function(data, textStatus, jqXHR) {
      midman_cache[midman_content_id] = data.html;
      midman_content.html(data.html);
    });
    return false;
  });

  $('.nav-alerts').click(function() {
    this_content_id = '.nav-alerts';
    if (midman_content_id == this_content_id) {
      midman_close(this_content_id)
    } else {
      midman_open(this_content_id)
    }
    return false;
  });
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