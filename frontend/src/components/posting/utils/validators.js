import { maxLength, minLength } from "misago/utils/validators"
import misago from "misago"

export function getTitleValidators() {
  return [getTitleLengthMin(), getTitleLengthMax()]
}

export function getPostValidators() {
  if (misago.get("SETTINGS").post_length_max) {
    return [validatePostLengthMin(), validatePostLengthMax()]
  } else {
    return [validatePostLengthMin()]
  }
}

export function getTitleLengthMin() {
  return minLength(
    misago.get("SETTINGS").thread_title_length_min,
    (limitValue, length) => {
      const message = npgettext(
        "thread title length validator",
        "Thread title should be at least %(limit_value)s character long (it has %(show_value)s).",
        "Thread title should be at least %(limit_value)s characters long (it has %(show_value)s).",
        limitValue
      )

      return interpolate(
        message,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  )
}

export function getTitleLengthMax() {
  return maxLength(
    misago.get("SETTINGS").thread_title_length_max,
    (limitValue, length) => {
      const message = npgettext(
        "thread title length validator",
        "Thread title cannot be longer than %(limit_value)s character (it has %(show_value)s).",
        "Thread title cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
        limitValue
      )

      return interpolate(
        message,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  )
}

export function validatePostLengthMin() {
  return minLength(
    misago.get("SETTINGS").post_length_min,
    (limitValue, length) => {
      const message = npgettext(
        "post length validator",
        "Posted message should be at least %(limit_value)s character long (it has %(show_value)s).",
        "Posted message should be at least %(limit_value)s characters long (it has %(show_value)s).",
        limitValue
      )

      return interpolate(
        message,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  )
}

export function validatePostLengthMax() {
  return maxLength(
    misago.get("SETTINGS").post_length_max || 1000000,
    (limitValue, length) => {
      const message = npgettext(
        "post length validator",
        "Posted message cannot be longer than %(limit_value)s character (it has %(show_value)s).",
        "Posted message cannot be longer than %(limit_value)s characters (it has %(show_value)s).",
        limitValue
      )

      return interpolate(
        message,
        {
          limit_value: limitValue,
          show_value: length,
        },
        true
      )
    }
  )
}
