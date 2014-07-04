$(function() {
  moment.lang($('html').attr('lang'))
  var moment_now = moment();
  var time_format = moment_now.lang()._longDateFormat.LT;

  var moments = {};

  // Initialize moment.js for dates
  $('.dynamic').each(function() {
    var timestamp = $(this).data('timestamp');
    var rel_moment = moment(timestamp);

    if (moment_now.diff(rel_moment, 'days') <= 7) {
      moments[timestamp] = {
        rel_moment: rel_moment,
        original: $(this).text()
      }
    }
  });

  // Update function
  function update_times() {
    $('.time-ago').each(function() {
      var timestamp = $(this).data('timestamp');
      if (moments[timestamp] != undefined) {
        if (moment_now.diff(moments[timestamp].rel_moment, 'hours') <= 6) {
          $(this).text(moments[timestamp].rel_moment.fromNow());
        } else if (moment_now.diff(moments[timestamp].rel_moment, 'days') < 2) {
          $(this).text(moments[timestamp].rel_moment.calendar());
        } else if (moment_now.diff(moments[timestamp].rel_moment, 'days') <= 7) {
          $(this).text(moments[timestamp].rel_moment.format("dddd, " + time_format));
        } else {
          $(this).text(moments[timestamp].original);
        }
      }
    });
  }

  // Run updates
  update_times();
  window.setInterval(update_times, 5000);
});
