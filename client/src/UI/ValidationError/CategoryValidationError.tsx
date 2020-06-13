import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
}

const CategoryValidationError: React.FC<IValidationErrorProps> = ({
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
          case "auth_error.not_moderator":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "auth_error.not_moderator.category"
                )`You can't moderate this category.`
              ),
            })

          case "auth_error.category.closed":
            return children({
              type: errorType,
              message: i18n._(
                t("auth_error.category.closed")`This category is closed.`
              ),
            })

          case "value_error.category.not_exists":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.category.not_exists"
                )`Category could not be found.`
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

export default CategoryValidationError
