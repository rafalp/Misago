import { plural, t } from "@lingui/macro"
import React from "react"
import ValidationError from "./ValidationError"
import { ValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  min: "value_error.any_str.min_length",
  max: "value_error.any_str.max_length",
}

const PasswordValidationError: React.FC<ValidationErrorProps> = ({
  children,
  error,
  messages,
  value = 0,
  min = 0,
  max = 0,
}) => {
  if (!error) return null

  const errorType = ERROR_TYPES_MAP[error.type] || error.type
  if (messages && messages[errorType]) {
    return children({ type: errorType, message: messages[errorType] })
  }

  switch (errorType) {
    case "value_error.missing":
      return children({
        type: errorType,
        message: t({
          id: "value_error.password.missing",
          message: "Password can't be empty.",
        }),
      })

    case "value_error.any_str.min_length":
      return children({
        type: errorType,
        message: t({
          id: "value_error.password.min_length",
          message: plural(min, {
            one: `Password should be at least # character long (it has ${value}).`,
            other: `Password should be at least # characters long (it has ${value}).`,
          }),
        }),
      })

    case "value_error.any_str.max_length":
      return children({
        type: errorType,
        message: t({
          id: "value_error.password.max_length",
          message: plural(max, {
            one: `Password should be no longer than # character (it has ${value}).`,
            other: `Password should be no longer than # characters (it has ${value}).`,
          }),
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default PasswordValidationError
