// Register tooltips
$(function() {
  $.misago_dom().change(function() {
    $('.tooltip-top').tooltip({container: 'body', placement: 'top'});
    $('.tooltip-bottom').tooltip({container: 'body', placement: 'bottom'});
    $('.tooltip-left').tooltip({container: 'body', placement: 'left'});
    $('.tooltip-right').tooltip({container: 'body', placement: 'right'});
    $('.tooltip-top, .tooltip-bottom, .tooltip-left, .tooltip-right').each(function() {
      $(this).tooltip('fixTitle');
    });
  });
});

// Helper for registering tooltips
function misago_tooltip(element) {
  placement = null;
  if (element.hasClass('tooltip-top')) {
    placement = 'top';
  } else if (element.hasClass('tooltip-bottom')) {
    placement = 'bottom';
  } else if (element.hasClass('tooltip-left')) {
    placement = 'left';
  } else if (element.hasClass('tooltip-right')) {
    placement = 'right';
  }

  if (placement) {
    element.tooltip({container: 'body', placement: placement})
  }
}
