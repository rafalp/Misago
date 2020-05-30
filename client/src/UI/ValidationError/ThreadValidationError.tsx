import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
}

const ThreadValidationError: React.FC<IValidationErrorProps> = ({
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
          case "auth_error.thread.closed":
            return children({
              type: errorType,
              message: i18n._(
                t("auth_error.thread.closed")`This thread is closed.`
              ),
            })

          case "value_error.thread.not_exists":
            return children({
              type: errorType,
              message: i18n._(
                t("value_error.thread.not_exists")`Thread could not be found.`
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

export default ThreadValidationError
