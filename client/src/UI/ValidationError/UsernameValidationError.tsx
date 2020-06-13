import { plural, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  matches: "value_error.username",
  min: "value_error.any_str.min_length",
  max: "value_error.any_str.max_length",
}

const UsernameValidationError: React.FC<IValidationErrorProps> = ({
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
              message: i18n._(
                t("value_error.username.missing")`User name can't be empty.`
              ),
            })

          case "value_error.username":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.username"
                )`User name can only contain latin alphabet letters and digits.`
              ),
            })

          case "value_error.username.not_available":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.username.not_available"
                )`This user name is not available.`
              ),
            })

          case "value_error.username.not_allowed":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.username.not_allowed"
                )`This user name is not allowed.`
              ),
            })

          case "value_error.any_str.min_length":
            return children({
              type: errorType,
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
              type: errorType,
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
