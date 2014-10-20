// Define extension
function enableYesNoSwitch(selector) {
  function createYesNoSwitch($control) {
    var name = $control.find('input').first().attr('name');
    var value = $control.find("input:checked").val() * 1;

    // hide original switch options
    $control.find('ul, label').addClass('hidden-original-switch');

    var yes_label = $.trim($control.find('label').first().text());
    var no_label = $.trim($control.find('label').last().text());

    var toggle_off = "fa fa-toggle-off fa-2x";
    var toggle_on = "fa fa-toggle-on fa-2x";

    // Render new switch
    var $new_switch = $('<label class="yes-no-switch"></label>');
    var $icon = $('<span class="' + toggle_off + '"></span>');
    var $label = $('<strong class="yes-no-label"></strong>');

    $control.prepend($new_switch);
    $new_switch.append($icon);
    $new_switch.append($label);

    if (value) {
      $new_switch.addClass('active');
      $icon.attr("class", toggle_on);
      $label.text(yes_label);
    } else {
      $icon.attr("class", toggle_off);
      $label.text(no_label);
    }

    $new_switch.click(function() {
      $this = $(this);

      if ($this.hasClass('active')) {
        new_value = 0;
        $this.removeClass('active');
        $icon.attr("class", toggle_off);
        $label.text(no_label);
      } else {
        new_value = 1;
        $this.addClass('active');
        $icon.attr("class", toggle_on);
        $label.text(yes_label);
      }

      $control.find('.yesno-switch').first().prop('checked', new_value == 1);
      $control.find('.yesno-switch').last().prop('checked', new_value == 0);
    });
  }

  $(selector).each(function() {
    if ($(this).data('misago-yes-no-switch') == undefined) {
      $(this).data('misago-yes-no-switch', 'ok');
      if ($(this).find('.yesno-switch').length == 2) {
        createYesNoSwitch($(this));
      }
    };
  });
}


// Enable switch
$(function() {
  enableYesNoSwitch('.control-radioselect');
  Misago.DOM.on_change(function() {
    enableYesNoSwitch('.control-radioselect');
  });
});
