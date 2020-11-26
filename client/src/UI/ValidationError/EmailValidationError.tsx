import { t } from "@lingui/macro"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  email: "value_error.email",
}

const EmailValidationError: React.FC<IValidationErrorProps> = ({
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
          id: "value_error.email.missing",
          message: "E-mail address can't be empty.",
        }),
      })

    case "value_error.email":
      return children({
        type: errorType,
        message: t({
          id: "value_error.email",
          message: "This e-mail address is not valid.",
        }),
      })

    case "value_error.email.not_available":
      return children({
        type: errorType,
        message: t({
          id: "value_error.email.not_available",
          message: "This e-mail address is not available.",
        }),
      })

    case "value_error.email.not_allowed":
      return children({
        type: errorType,
        message: t({
          id: "value_error.email.not_allowed",
          message: "This e-mail address is not allowed.",
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default EmailValidationError
