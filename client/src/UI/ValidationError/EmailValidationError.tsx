import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  "required": "value_error.missing",
  "email": "value_error.email",
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

  return (
    <I18n>
      {({ i18n }) => {
        switch (errorType) {
          case "value_error.missing":
            return children({
              type: errorType,
              message: i18n._(t("value_error.email.missing")`E-mail address can't be empty.`),
            })

          case "value_error.email":
            return children({
              type: errorType,
              message: i18n._(t("value_error.email")`This e-mail address is not valid.`),
            })

          case "value_error.email.not_available":
            return children({
              type: errorType,
              message: i18n._(t("value_error.email.not_available")`This e-mail address is not available.`),
            })

          default:
            return (
              <ValidationError error={error} value={value} min={min} max={max}>
                {children}
              </ValidationError>
            )
        }
      }}
    </I18n>
  )
}

export default EmailValidationError
