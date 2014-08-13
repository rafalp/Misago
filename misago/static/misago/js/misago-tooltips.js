// Register tooltips
$(function() {
  $.misago_dom().change(function() {
    $('.tooltip-top').tooltip({placement: 'top'});
    $('.tooltip-bottom').tooltip({placement: 'bottom'});
    $('.tooltip-left').tooltip({placement: 'left'});
    $('.tooltip-right').tooltip({placement: 'right'});
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
    element.tooltip({placement: placement})
  }
}
