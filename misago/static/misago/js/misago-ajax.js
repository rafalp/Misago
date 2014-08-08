// Misago ajax error handler
$(function() {
  function handleAjaxError(event, jqxhr, settings, thrownError) {
    console.log(jqxhr);
    if (jqxhr.responseJSON) {
      var error_message = jqxhr.responseJSON.message
    } else if (thrownError == "NOT FOUND") {
      var error_message = ajax_errors.not_found;
    } else if (thrownError == "timeout") {
      var error_message = ajax_errors.timeout;
    } else {
      var error_message = ajax_errors.generic;
    }
    console.log(thrownError);
    if (thrownError != "") {
      $.misago_alerts().error(error_message);
    }
  }
  $(document).ajaxError(handleAjaxError);
});
