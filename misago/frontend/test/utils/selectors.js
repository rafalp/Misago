(function () {
  'use strict';

  window.getElement = function(selector) {
    return $('#misago-fixture ' + selector);
  };

  window.getElementText = function(selector) {
    return $.trim(getElement(selector).text());
  };

  window.getAlertType = function() {
    var alertClass = $('.alerts .alert').attr("class");

    if (alertClass.indexof('alert-info') >= 0) {
      return 'info';
    } else if (alertClass.indexof('alert-success') >= 0) {
      return 'success';
    } else if (alertClass.indexof('alert-warning') >= 0) {
      return 'warning';
    } else if (alertClass.indexof('alert-danger') >= 0) {
      return 'error';
    } else {
      return null;
    }
  };

  window.getAlertMessage = function() {
    return getElementText('.alerts .alert');
  };

  window.getFieldFeedback = function(fieldId) {
    return $.trim($('#' + fieldId).parent().find('.errors').text());
  };
}());
