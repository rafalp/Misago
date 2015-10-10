(function (Misago) {
  'use strict';

  // Validators namespace
  Misago.validators = {
    required: function() {
      return function(value) {
        if ($.trim(value).length === 0) {
          return gettext("This field is required.");
        }
      };
    }
  };

  var validate = function(ctrl) {
    var errors = {};
    var value = null;
    var validator = null;
    var result = null;

    for (var key in ctrl.validation) {
      if (ctrl.validation.hasOwnProperty(key)) {
        value = ctrl[key]();

        for (var i in ctrl.validation[key]) {
          validator = ctrl.validation[key][i];
          result = validator(value);

          if (result) {
            if (!errors[key]) {
              errors[key] = [];
            }
            errors[key].push(result);
          }
        }
      }
    }

    if (Object.getOwnPropertyNames(errors).length > 0) {
      return errors;
    } else {
      return null;
    }
  };

  Misago.addService('validate', {
    factory: function() {
      return validate;
    }
  });
}(Misago.prototype));
