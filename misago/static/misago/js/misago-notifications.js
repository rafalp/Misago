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

    if (ajax_cache != null && data.count != ajax_cache.count) {
      ajax_cache = null;
      if ($container.hasClass('open')) {
        $container.find('.btn-refresh').fadeIn();
        if (data.count > 0) {
          $container.find('.btn-read-all').fadeIn();
        } else {
          $container.find('.btn-read-all').fadeOut();
        }
      }
    }
  }

  if (is_authenticated) {
    $.misago_ui().observer("misago_notifications", notifications_handler);
  }

  var $display = $container.find('.display');
  var $loader = $container.find('.loader');

  function handle_list_response(data) {
    ajax_cache = data;
    $loader.hide();
    $display.html(data.html);
    $display.show();
    $.misago_dom().changed();
    $link.tooltip('destroy');
  }

  function fetch_list() {
    $.get($link.attr('href'), function(data) {
      handle_list_response(data)
    });
  }

  $container.on('click', '.btn-refresh', function() {
    $display.hide();
    $loader.show();
    fetch_list();
    $link.tooltip('destroy');
  });
  $container.on('show.bs.dropdown', function () {
    if (ajax_cache == null) {
      fetch_list();
    } else {
      $link.tooltip('destroy');
    }
  });
  $container.on('hide.bs.dropdown', function() {
    misago_tooltip($link);
    $container.find('.btn-refresh').hide();
  });
  $container.on('submit', '.read-all-notifications', function() {
    $display.hide();
    $loader.show();
    $.post($link.attr('href'), $(this).serialize(), function(data) {
      handle_list_response(data);
      $.misago_ui().query_server();
    });
    return false;
  });
});
