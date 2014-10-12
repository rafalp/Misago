$(function() {
  var $nav = $('#main-navbar');

  if (is_authenticated) {
    // badges updates
    $.misago_ui().observer(function(data) {
      $nav.find('.badge').each(function() {
        var binding_name = $(this).data('badge-binding');
        if (binding_name != undefined && data[binding_name].count != undefined) {
          var count = data[binding_name].count;
          $(this).text(count);
          if (count > 0) {
            $(this).addClass("in");
          } else {
            $(this).removeClass("in");
          }
        }
      });
    });

    // tooltips updates
    $.misago_ui().observer(function(data) {
      $nav.find('.tooltip-bottom').each(function() {
        var binding_name = $(this).data('tooltip-binding');
        if (binding_name != undefined && data[binding_name].message != undefined) {
          $(this).attr("title", data[binding_name].message);
        }
      });
    });
  }
});
