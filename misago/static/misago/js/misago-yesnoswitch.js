// Define extension
function enableYesNoSwitch(selector, yes, no) {
  function realYesNoSwitch(control) {
    var name = control.find('.yesno-switch').first().attr('name');
    var value = control.find('.yesno-switch').filter(":checked").val() * 1;

    var buttons = $('<div class="btn-group yes-no-switch">' +
      '<button type="button" class="btn btn-yes btn-default">' + yes + '</button>' +
      '<button type="button" class="btn btn-no btn-default">' + no + '</button>' +
    '</div>');

    var button_yes = buttons.find('.btn-yes');
    var button_no = buttons.find('.btn-no');

    control.find('.yesno-switch').first().parent().before(buttons);
    control.find('.yesno-switch').parent().addClass('ninja-switch');

    function switchState(newstate) {
      function switchToYes() {
        button_yes.addClass('active');
        button_yes.addClass('btn-success');
        button_yes.removeClass('btn-default');
        button_no.removeClass('active');
        button_no.addClass('btn-default');
        button_no.removeClass('btn-danger');
      }

      function switchToNo() {
        button_yes.removeClass('active');
        button_yes.removeClass('btn-success');
        button_yes.addClass('btn-default');
        button_no.addClass('active');
        button_no.removeClass('btn-default');
        button_no.addClass('btn-danger');
      }

      if (newstate == 1) {
        switchToYes();
      } else {
        switchToNo();
      }

      control.find('.yesno-switch').first().prop('checked', newstate == 1);
      control.find('.yesno-switch').last().prop('checked', newstate == 0);
    }

    switchState(value);

    button_yes.click(function() {
      switchState(1);
    });

    button_no.click(function() {
      switchState(0);
    });
  }

  $(selector).each(function() {
    if ($(this).find('.yesno-switch').length == 2) {
      realYesNoSwitch($(this));
    }
  });
}


// Enable switch
$(function() {
  enableYesNoSwitch('.control-radioselect', lang_yes, lang_no);
});
