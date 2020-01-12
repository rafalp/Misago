import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const EmailValidationError: React.FC<IValidationErrorProps> = ({
  children,
  error,
  messages,
  value = 0,
  min = 0,
  max = 0,
}) => {
  if (!error) return null
  if (messages && messages[error]) {
    return children({ type: error, message: messages[error] })
  }

  return (
    <I18n>
      {({ i18n }) => {
        switch (error) {
          case "value_error.missing":
            return children({
              type: error,
              message: i18n._(t("value_error.username.missing")`E-mail address can't be empty.`),
            })

          case "value_error.email":
            return children({
              type: error,
              message: i18n._(t("value_error.email")`This e-mail address is not valid.`),
            })

          case "value_error.email.not_available":
            return children({
              type: error,
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
