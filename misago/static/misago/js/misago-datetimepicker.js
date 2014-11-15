// Form enchancer for datetimes
$(function() {

  function enchanceDateTimeField($control) {

    var formats = $control.data('input-format').split(" ");
    var date_format = formats[0];
    var time_format = formats[1].replace(":%S", "");

    var $input = $control.find('input');

    $input.attr('type', 'hidden');

    var $date = $('<input type="text"  class="form-control" style="float: left; width: 108px; margin-right: 8px; text-align: center;">');
    var $time = $('<input type="text" class="form-control" style="float: left; width: 68px; text-align: center;">');

    var $container = $('<div style="overflow: auto;"></div>');

    $container.insertAfter($input);

    $container.append($date);
    $container.append($time);

    date_format = date_format.replace('%d', 'DD');
    date_format = date_format.replace('%m', 'MM');
    date_format = date_format.replace('%y', 'YY');
    date_format = date_format.replace('%Y', 'YYYY');

    $date.datetimepicker({
      format: date_format,
      pickDate: true,
      pickTime: false
    });

    var values = $input.val().split(" ");
    if (values.length == 2) {
      $date.val(values[0]);

      var time = values[1].split(":");
      $time.val(time[0] + ":" + time[1]);
    }

    $time.datetimepicker({
      format: 'HH:mm',
      pickDate: false,
      pickSeconds: false,
      pick12HourFormat: false
    });

    function update_value() {
      $input.val($date.val() + " " + $time.val());
    }

    $date.change(update_value);
    $time.change(update_value);
  }

  // discover formatted fields
  $('.controls').each(function() {
    if ($(this).data('input-format')) {
      enchanceDateTimeField($(this));
    }
  })

})
