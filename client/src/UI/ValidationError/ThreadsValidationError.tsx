import { plural, t } from "@lingui/macro"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  min: "value_error.list.min_items",
  max: "value_error.list.max_items",
}

const ThreadsValidationError: React.FC<IValidationErrorProps> = ({
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
    case "value_error.list.min_items":
      return children({
        type: errorType,
        message: t({
          id: "value_error.threads.min_items",
          message: plural(min, {
            one: "Select at least # thread.",
            other: "Select at least # threads.",
          }),
        }),
      })

    case "value_error.list.max_items":
      return children({
        type: errorType,
        message: t({
          id: "value_error.threads.max_items",
          message: plural(max, {
            one: `You can't select more than # thread (you've selected ${value}).`,
            other: `You can't select more than # threads (you've selected ${value}).`,
          }),
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default ThreadsValidationError
