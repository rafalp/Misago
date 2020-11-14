import { t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
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
  const { i18n } = useLingui()

  if (!error) return null

  const errorType = ERROR_TYPES_MAP[error.type] || error.type
  if (messages && messages[errorType]) {
    return children({ type: errorType, message: messages[errorType] })
  }

  switch (errorType) {
    case "auth_error.not_moderator":
      return children({
        type: errorType,
        message: i18n._(
          "auth_error.not_moderator.thread",
          t`You can't moderate this thread.`
        ),
      })

    case "auth_error.category.closed":
      return children({
        type: errorType,
        message: i18n._(
          "auth_error.thread_category.closed",
          t`This thread's category is closed.`
        ),
      })

    case "auth_error.thread.closed":
      return children({
        type: errorType,
        message: i18n._("auth_error.thread.closed", t`This thread is closed.`),
      })

    case "auth_error.thread.not_author":
      return children({
        type: errorType,
        message: i18n._(
          "auth_error.thread.not_author",
          t`You need to be this thread's author to perform this action.`
        ),
      })

    case "value_error.thread.not_exists":
      return children({
        type: errorType,
        message: i18n._(
          "value_error.thread.not_exists",
          t`Thread could not be found.`
        ),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default ThreadValidationError
