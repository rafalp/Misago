const EMAIL = /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i;
const USERNAME = new RegExp('^[0-9a-z]+$', 'i');

export function required() {
  return function(value) {
    if ($.trim(value).length === 0) {
      return gettext("This field is required.");
    }
  };
}

export function email(message) {
  return function(value) {
    if (!EMAIL.test(value)) {
      return message || gettext("Enter a valid email address.");
    }
  };
}

export function minLength(limitValue, message) {
  return function(value) {
    var returnMessage = '';
    var length = $.trim(value).length;

    if (length < limitValue) {
      if (message) {
        returnMessage = message(limitValue, length);
      } else {
        returnMessage = ngettext(
          "Ensure this value has at least %(limit_value)s character (it has %(show_value)s).",
          "Ensure this value has at least %(limit_value)s characters (it has %(show_value)s).",
          limitValue);
      }
      return interpolate(returnMessage, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }
  };
}

export function maxLength(limitValue, message) {
  return function(value) {
    var returnMessage = '';
    var length = $.trim(value).length;

    if (length > limitValue) {
      if (message) {
        returnMessage = message(limitValue, length);
      } else {
        returnMessage = ngettext(
          "Ensure this value has at most %(limit_value)s character (it has %(show_value)s).",
          "Ensure this value has at most %(limit_value)s characters (it has %(show_value)s).",
          limitValue);
      }
      return interpolate(returnMessage, {
        limit_value: limitValue,
        show_value: length
      }, true);
    }
  };
}

export function usernameMinLength(settings) {
  var message = function(limitValue) {
    return ngettext(
      "Username must be at least %(limit_value)s character long.",
      "Username must be at least %(limit_value)s characters long.",
      limitValue);
  };
  return this.minLength(settings.username_length_min, message);
}

export function usernameMaxLength(settings) {
  var message = function(limitValue) {
    return ngettext(
      "Username cannot be longer than %(limit_value)s character.",
      "Username cannot be longer than %(limit_value)s characters.",
      limitValue);
  };
  return this.maxLength(settings.username_length_max, message);
}

export function usernameContent() {
  return function(value) {
    if (!USERNAME.test($.trim(value))) {
      return gettext("Username can only contain latin alphabet letters and digits.");
    }
  };
}

export function passwordMinLength(settings) {
  var message = function(limitValue) {
    return ngettext(
      "Valid password must be at least %(limit_value)s character long.",
      "Valid password must be at least %(limit_value)s characters long.",
      limitValue);
  };
  return this.minLength(settings.password_length_min, message);
}