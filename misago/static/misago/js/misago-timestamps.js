$(function() {
  moment.lang($('html').attr('lang'))

  if (lang_time_units === undefined) {
    var units_formats = "smhd";
  } else {
    var units_formats = lang_time_units;
  }

  var moment_now = moment();
  var time_format = moment_now.lang()._longDateFormat.LT;

  var moments = {};

  // Initialize moment.js for dates
  function discover_dates() {
    $('.dynamic').each(function() {
      var timestamp = $(this).data('timestamp');
      var rel_moment = moment(timestamp);

      moments[timestamp] = {
        rel_moment: rel_moment,
        original: $(this).text()
      }
    });
  }
  discover_dates();

  // Update function
  function update_times() {
    $('.time-ago').each(function() {
      var timestamp = $(this).data('timestamp');

      if (moment_now.diff(moments[timestamp].rel_moment, 'minutes') <= 6 && moment_now.diff(moments[timestamp].rel_moment, 'hours') >= -6) {
        $(this).text(moments[timestamp].rel_moment.fromNow());
      } else if (moment_now.diff(moments[timestamp].rel_moment, 'days') < 1 && moment_now.diff(moments[timestamp].rel_moment, 'days') > -1) {
        $(this).text(moments[timestamp].rel_moment.calendar());
      } else if (moment_now.diff(moments[timestamp].rel_moment, 'days') < 7 && moment_now.diff(moments[timestamp].rel_moment, 'days') > -7) {
        $(this).text(moments[timestamp].rel_moment.format("dddd, " + time_format));
      } else {
        $(this).text(moments[timestamp].original);
      }
    });

    $('.time-ago-compact').each(function() {
      var timestamp = $(this).data('timestamp');
      var diff_seconds = moment_now.diff(moments[timestamp].rel_moment, 'seconds');

      if (diff_seconds < 60) {
        $(this).text(diff_seconds + units_formats[0]);
      } else if (diff_seconds < (60 * 56)) {
        var diff_minutes = Math.floor(diff_seconds / 60);
        $(this).text(diff_minutes + units_formats[1]);
      } else if (diff_seconds <= (3600 * 23)) {
        var diff_hours = Math.floor(diff_seconds / 3600);
        $(this).text(diff_hours + units_formats[2]);
      } else if (true | diff_seconds < (3600 * 24 * 15)) {
        var diff_days = Math.floor(diff_seconds / (3600 * 24));
        $(this).text(diff_days + units_formats[3]);
      } else {
        $(this).text(moments[timestamp].original);
      }
    });
  }

  // Run updates
  $.misago_dom().change(discover_dates);
  $.misago_dom().change(update_times);
  window.setInterval(update_times, 5000);
});
