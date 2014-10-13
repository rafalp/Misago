// Fancy data-bound tooltips
$(function() {
  function set_tooltips() {
    $('.tooltip-top').tooltip({container: 'body', placement: 'top'});
    $('.tooltip-bottom').tooltip({container: 'body', placement: 'bottom'});
    $('.tooltip-left').tooltip({container: 'body', placement: 'left'});
    $('.tooltip-right').tooltip({container: 'body', placement: 'right'});
  }

  function bind_tooltips(data) {
    $('[data-misago-tooltip]').each(function() {
      var new_tooltip = Misago.getattr(data, $(this).data('misago-tooltip'));
      if (new_tooltip != undefined) {
        $(this).attr("title", new_tooltip);
        $(this).tooltip('fixTitle');
      }
    });
  }

  // Bind tooltips to DOM
  bind_tooltips();
  Misago.set_tooltips = set_tooltips;
  Misago.DOM.on_change(set_tooltips);
  Misago.Server.on_data(bind_tooltips);
});
