import { t } from "@lingui/macro"
import React from "react"
import ValidationError from "./ValidationError"
import { ValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
}

const ThreadValidationError: React.FC<ValidationErrorProps> = ({
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
    case "auth_error.not_moderator":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.not_moderator.thread",
          message: "You can't moderate this thread.",
        }),
      })

    case "auth_error.category.closed":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.thread_category.closed",
          message: "This thread's category is closed.",
        }),
      })

    case "auth_error.thread.closed":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.thread.closed",
          message: "This thread is closed.",
        }),
      })

    case "auth_error.thread.not_author":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.thread.not_author",
          message:
            "You need to be this thread's author to perform this action.",
        }),
      })

    case "value_error.thread.not_exists":
      return children({
        type: errorType,
        message: t({
          id: "value_error.thread.not_exists",
          message: "Thread could not be found.",
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default ThreadValidationError
