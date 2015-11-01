(function (Misago) {
  'use strict';

  var EMAIL = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
  var USERNAME = new RegExp('^[0-9a-z]+$', 'i');

  // Validators namespace
  Misago.validators = {
    required: function() {
      return function(value) {
        if ($.trim(value).length === 0) {
          return gettext("This field is required.");
        }
      };
    },
    email: function(message) {
      return function(value) {
        if (!EMAIL.test(value)) {
          return message || gettext("Enter a valid email address.");
        }
      };
    },
    minLength: function(limit_value, message) {
      return function(value) {
        var returnMessage = '';
        var length = $.trim(value).length;

        if (length < limit_value) {
          if (message) {
            returnMessage = message(limit_value, length);
          } else {
            returnMessage = ngettext(
              "Ensure this value has at least %(limit_value)s character (it has %(show_value)s).",
              "Ensure this value has at least %(limit_value)s characters (it has %(show_value)s).",
              limit_value);
          }
          return interpolate(returnMessage, {
            limit_value: limit_value,
            show_value: length
          }, true);
        }
      };
    },
    maxLength: function(limit_value, message) {
      return function(value) {
        var returnMessage = '';
        var length = $.trim(value).length;

        if (length > limit_value) {
          if (message) {
            returnMessage = message(limit_value, length);
          } else {
            returnMessage = ngettext(
              "Ensure this value has at most %(limit_value)s character (it has %(show_value)s).",
              "Ensure this value has at most %(limit_value)s characters (it has %(show_value)s).",
              limit_value);
          }
          return interpolate(returnMessage, {
            limit_value: limit_value,
            show_value: length
          }, true);
        }
      };
    },
    usernameMinLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Username must be at least %(limit_value)s character long.",
          "Username must be at least %(limit_value)s characters long.",
          limit_value);
      };
      return this.minLength(settings.username_length_min, message);
    },
    usernameMaxLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Username cannot be longer than %(limit_value)s character.",
          "Username cannot be longer than %(limit_value)s characters.",
          limit_value);
      };
      return this.maxLength(settings.username_length_max, message);
    },
    usernameContent: function() {
      return function(value) {
        if (!USERNAME.test($.trim(value))) {
          return gettext("Username can only contain latin alphabet letters and digits.");
        }
      };
    },
    passwordMinLength: function(settings) {
      var message = function(limit_value) {
        return ngettext(
          "Valid password must be at least %(limit_value)s character long.",
          "Valid password must be at least %(limit_value)s characters long.",
          limit_value);
      };
      return this.minLength(settings.password_length_min, message);
    }
  };

  var validateField = function(value, validators) {
    var result = Misago.validators.required()(value);
    var errors = [];

    if (result) {
      return [result];
    } else {
      for (var i in validators) {
        result = validators[i](value);

        if (result) {
          errors.push(result);
        }
      }
    }

    return errors.length ? errors : true;
  };

  var validateForm = function(form) {
    var errors = {};
    var value = null;

    var isValid = true;

    for (var key in form.validation) {
      if (form.validation.hasOwnProperty(key)) {
        value = form[key]();
        errors[key] = validateField(form[key](), form.validation[key]);
        if (errors[key] !== true) {
          isValid = false;
        }
      }
    }

    form.errors = errors;
    return isValid;
  };

  var validate = function(form, name) {
    if (name) {
      return function(value) {
        var errors = null;
        if (typeof value !== 'undefined') {
          errors = validateField(value, form.validation[name]);
          if (errors) {
            if (!form.errors) {
              form.errors = {};
            }
            form.errors[name] = errors;
          }
          form[name](value);
          return form[name](value);
        } else {
          return form[name]();
        }
      };
    } else {
      return validateForm(form);
    }
  };

  Misago.addService('validate', {
    factory: function() {
      return validate;
    }
  });
}(Misago.prototype));
