import { plural } from "@lingui/macro"
import { I18n } from "@lingui/react"
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

  return (
    <I18n>
      {({ i18n }) => {
        switch (errorType) {
          case "value_error.list.min_items":
            return children({
              type: errorType,
              message: i18n._(
                plural("value_error.threads.min_items", {
                  value: min,
                  one: `Select at least # thread.`,
                  other: `Select at least # threads.`,
                })
              ),
            })

          case "value_error.list.max_items":
            return children({
              type: errorType,
              message: i18n._(
                plural("value_error.threads.max_items", {
                  value: max,
                  one: `You can't select more than # thread (you've selected ${value}).`,
                  other: `You can't select more than # threads (you've selected ${value}).`,
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

export default ThreadsValidationError
