import { t } from "@lingui/macro"
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

  switch (errorType) {
    case "value_error.missing":
      return children({
        type: errorType,
        message: t({
          id: "value_error.category.missing",
          message: "Thread category can't be empty.",
        }),
      })

    case "auth_error.not_moderator":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.not_moderator.category",
          message: "You can't moderate this category.",
        }),
      })

    case "auth_error.category.closed":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.category.closed",
          message: "This category is closed.",
        }),
      })

    case "value_error.category.not_exists":
      return children({
        type: errorType,
        message: t({
          id: "value_error.category.not_exists",
          message: "Category could not be found.",
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default CategoryValidationError
