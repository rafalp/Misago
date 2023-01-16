const EMAIL =
  /^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i
const USERNAME = new RegExp("^[0-9a-z]+$", "i")

export function required(message) {
  return function (value) {
    if (value === false || value === null || $.trim(value).length === 0) {
      return message || gettext("This field is required.")
    }
  }
}

export function requiredTermsOfService(message) {
  const error = gettext("You have to accept the terms of service.")
  return required(message || error)
}

export function requiredPrivacyPolicy(message) {
  const error = gettext("You have to accept the privacy policy.")
  return required(message || error)
}

export function email(message) {
  return function (value) {
    if (!EMAIL.test(value)) {
      return message || gettext("Enter a valid email address.")
    }
  }
}

export function minLength(limitValue, message) {
  return function (value) {
    var returnMessage = ""
    var length = $.trim(value).length

    if (length < limitValue) {
      if (message) {
        returnMessage = message(limitValue, length)
      } else {
        returnMessage = ngettext(
          "Ensure this value has at least %(limit_value)s character (it has %(show_value)s).",
          "Ensure this value has at least %(limit_value)s characters (it has %(show_value)s).",
          limitValue
        )
      }
      return interpolate(
        returnMessage,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  }
}

export function maxLength(limitValue, message) {
  return function (value) {
    var returnMessage = ""
    var length = $.trim(value).length

    if (length > limitValue) {
      if (message) {
        returnMessage = message(limitValue, length)
      } else {
        returnMessage = ngettext(
          "Ensure this value has at most %(limit_value)s character (it has %(show_value)s).",
          "Ensure this value has at most %(limit_value)s characters (it has %(show_value)s).",
          limitValue
        )
      }
      return interpolate(
        returnMessage,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  }
}

export function usernameMinLength(lengthMin) {
  var message = function (lengthMin) {
    return ngettext(
      "Username must be at least %(limit_value)s character long.",
      "Username must be at least %(limit_value)s characters long.",
      lengthMin
    )
  }
  return minLength(lengthMin, message)
}

export function usernameMaxLength(lengthMax) {
  var message = function (lengthMax) {
    return ngettext(
      "Username cannot be longer than %(limit_value)s character.",
      "Username cannot be longer than %(limit_value)s characters.",
      lengthMax
    )
  }
  return maxLength(lengthMax, message)
}

export function usernameContent() {
  return function (value) {
    if (!USERNAME.test($.trim(value))) {
      return gettext(
        "Username can only contain latin alphabet letters and digits."
      )
    }
  }
}

export function passwordMinLength(limitValue) {
  return function (value) {
    const length = value.length

    if (length < limitValue) {
      const returnMessage = ngettext(
        "Valid password must be at least %(limit_value)s character long.",
        "Valid password must be at least %(limit_value)s characters long.",
        limitValue
      )

      return interpolate(
        returnMessage,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  }
}
