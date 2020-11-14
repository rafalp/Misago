import { plural, t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  min: "value_error.any_str.min_length",
  max: "value_error.any_str.max_length",
}

const PasswordValidationError: React.FC<IValidationErrorProps> = ({
  children,
  error,
  messages,
  value = 0,
  min = 0,
  max = 0,
}) => {
  const { i18n } = useLingui()

  if (!error) return null

  const errorType = ERROR_TYPES_MAP[error.type] || error.type
  if (messages && messages[errorType]) {
    return children({ type: errorType, message: messages[errorType] })
  }

  switch (errorType) {
    case "value_error.missing":
      return children({
        type: errorType,
        message: i18n._(
          "value_error.password.missing",
          t`Password can't be empty.`
        ),
      })

    case "value_error.any_str.min_length":
      return children({
        type: errorType,
        message: i18n._(
          "value_error.password.min_length",
          plural(min, {
            one: `Password should be at least # character long (it has ${value}).`,
            other: `Password should be at least # characters long (it has ${value}).`,
          })
        ),
      })

    case "value_error.any_str.max_length":
      return children({
        type: errorType,
        message: i18n._(
          "value_error.password.max_length",
          plural(max, {
            one: `Password should be no longer than # character (it has ${value}).`,
            other: `Password should be no longer than # characters (it has ${value}).`,
          })
        ),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default PasswordValidationError
