// Form enchancer for datetimes
$(function() {

  function enchanceDateTimeField($control) {

    var $input = $control.find('input');

    $input.attr('type', 'hidden');

    var $date = $('<input type="text"  class="form-control" style="float: left; width: 108px; margin-right: 8px; text-align: center;">');
    var $time = $('<input type="text" class="form-control" style="float: left; width: 68px; text-align: center;">');

    var $container = $('<div style="overflow: auto;"></div>');

    $container.insertAfter($input);

    $container.append($date);
    $container.append($time);

    if ($.trim($input.val()).length > 0) {
      var parsed = moment($input.val());
      if (parsed.isValid()) {
        $date.val(parsed.format('MM-DD-YYYY'));
        $time.val(parsed.format('HH:mm'));
      }
    }

    $date.datetimepicker({
      format: 'MM-DD-YYYY',
      pickDate: true,
      pickTime: false
    });

    $time.datetimepicker({
      format: 'HH:mm',
      pickDate: false,
      pickSeconds: false,
      pick12HourFormat: false
    });

    function update_value() {
      var input = moment($date.val() + " " + $time.val(), 'MM-DD-YYYY HH:mm');
      if (input.isValid()) {
        $input.val(input.format());
      } else {
        $input.val('');
      }
    }

    $date.change(update_value);
    $time.change(update_value);
  }

  // discover formatted fields
  $('.controls').each(function() {
    if ($(this).data('input-format')) {
      enchanceDateTimeField($(this));
    }
  });

});
