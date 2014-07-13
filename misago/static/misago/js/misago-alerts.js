// Alerts interactivity
$(function() {
  var $alerts = $('.misago-alerts');
  var $alerts_list = $('.misago-alerts .alerts-list');

  // Store and freeze alerts list height for affix
  var $height = $alerts.height();
  $alerts.height($height);

  // Affix alerts
  $('.misago-alerts .alerts-list').affix({
      offset: {
        top: $alerts.offset().top
      }
    });

  // Slide up alert
  $alerts.find('.close').click(function() {
    var $alert = $(this).parent().parent();
    $alerts.animate({height: $height - $alert.height()}, {queue: false});
    $alert.slideUp();
  });
});
