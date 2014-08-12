$(function() {
  var ajax_cache = null;

  var $container = $('.user-notifications-nav');
  var $link = $container.children('a');

  function notifications_handler(data) {
    var $badge = $link.children('.badge');

    if (data.count > 0) {
      if ($badge.length == 0) {
        $badge = $('<span class="badge">' + data.count + '</span>');
        $badge.hide();
        $link.append($badge);
        $badge.fadeIn();
      } else {
        $badge.text(data.count);
      }
    } else if ($badge.length > 0) {
        $badge.fadeOut();
    }
    $link.attr("title", data.message);
    $link.tooltip('fixTitle');

    if (ajax_cache != null && data.count != ajax_cache.count) {
      ajax_cache = null
    }
  }

  if (is_authenticated) {
    $.misago_ui().observer("misago_notifications", notifications_handler);
  }

  var $display = $container.find('.display');
  var $loader = $container.find('.loader');

  $container.on('show.bs.dropdown', function () {
    if (ajax_cache == null) {
      $.get($link.attr('href'), function(data) {
        ajax_cache = data;
        $loader.hide();
        $display.html(data.html);
        $.misago_dom().changed();
      });
    }
  })
});
