import { plural, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const UsernameValidationError: React.FC<IValidationErrorProps> = ({
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
              message: i18n._(t("value_error.username.missing")`User name can't be empty.`),
            })

          case "value_error.username":
            return children({
              type: error,
              message: i18n._(t("value_error.username")`User name can only contain latin alphabet letters and digits.`),
            })

          case "value_error.username.not_available":
            return children({
              type: error,
              message: i18n._(t("value_error.username.not_available")`This user name is not available.`),
            })

          case "value_error.any_str.min_length":
            return children({
              type: error,
              message: i18n._(
                plural("value_error.username.min_length", {
                  value: min,
                  one: `User name should be at least # character long (it has ${value}).`,
                  other: `User name should be at least # characters long (it has ${value}).`,
                })
              ),
            })

          case "value_error.any_str.max_length":
            return children({
              type: error,
              message: i18n._(
                plural("value_error.username.max_length", {
                  value: max,
                  one: `User name should be no longer than # character (it has ${value}).`,
                  other: `User name should be no longer than # characters (it has ${value}).`,
                })
              ),
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

export default UsernameValidationError
