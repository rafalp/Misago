// Misago ajax error handler
$(function() {
  function handleAjaxError(event, jqxhr, settings, thrownError) {
    if (jqxhr.responseJSON) {
      var error_message = jqxhr.responseJSON.message
    } else if (thrownError == "NOT FOUND") {
      var error_message = ajax_errors.not_found;
    } else if (thrownError == "timeout") {
      var error_message = ajax_errors.timeout;
    } else {
      var error_message = ajax_errors.generic;
    }

    if (thrownError != "") {
      Misago.Alerts.error(error_message);
    }
  }
  $(document).ajaxError(handleAjaxError);
});
