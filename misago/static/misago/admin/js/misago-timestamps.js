$(function() {
  moment.lang($('html').attr('lang'))
  var moment_now = moment();
  var time_format = moment_now.lang()._longDateFormat.LT;

  function set_titles() {
    $('.moment').each(function() {
      var obj = moment($(this).data('iso'));
      $(this).attr('title', obj.format('LLLL'));
    });
  }
  set_titles();

  function update_timestamps() {
    var now = moment();

    $('.moment').each(function() {
      var obj = moment($(this).data('iso'));
      var diff = Math.abs(obj.diff(now, 'seconds'));
      if (diff < 18000) {
        $(this).text(obj.from(now));
      } else {
        diff = Math.abs(obj.diff(now, 'days'));
        if (diff < 5) {
          $(this).text(obj.calendar(now));
        } else {
          $(this).text(obj.format($(this).data('format')));
        }
      }
    });

    $('.moment-length').each(function() {
      var minutes = $(this).data('minutes');
      var obj = moment.duration(minutes, 'minutes');
      $(this).text(obj.humanize());
    });
  }

  // Run updates
  update_timestamps();
  window.setInterval(update_timestamps, 5000);
});
