$(function() {
  var ajax_cache = null;

  var $container = $('.user-notifications-nav');
  var $link = $container.find('.dropdown-toggle');

  if (is_authenticated) {
    Misago.Server.on_data("notifications", function(data) {
      Tinycon.setBubble(data.count);
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
    });
  }

  var $display = $container.find('.display');
  var $loader = $container.find('.loader');

  function handle_list_response(data) {
    ajax_cache = data;
    $loader.hide();
    $display.html(data.html);
    $display.show();
    Misago.DOM.changed();
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
  });
  $container.on('show.bs.dropdown', function () {
    if (ajax_cache == null) {
      fetch_list();
    }
  });
  $container.on('hide.bs.dropdown', function() {
    $container.find('.btn-refresh').hide();
  });
  $container.on('submit', '.read-all-notifications', function() {
    $display.hide();
    $loader.show();
    $.post($link.attr('href'), $(this).serialize(), function(data) {
      handle_list_response(data);
      Misago.Server.update()
    });
    return false;
  });
});
