import { plural, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  matches: "value_error.thread_title",
  min: "value_error.any_str.min_length",
  max: "value_error.any_str.max_length",
}

const ThreadTitleValidationError: React.FC<IValidationErrorProps> = ({
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
                t(
                  "value_error.thread_title.missing"
                )`Thread title can't be empty.`
              ),
            })

          case "value_error.thread_title":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.thread_title"
                )`Thread title must contain latin alphabet letters and digits.`
              ),
            })

          case "value_error.thread_title.not_allowed":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.thread_title.not_allowed"
                )`This thread title is not allowed.`
              ),
            })

          case "value_error.any_str.min_length":
            return children({
              type: errorType,
              message: i18n._(
                plural("value_error.thread_title.min_length", {
                  value: min,
                  one: `Thread title should be at least # character long (it has ${value}).`,
                  other: `Thread title should be at least # characters long (it has ${value}).`,
                })
              ),
            })

          case "value_error.any_str.max_length":
            return children({
              type: errorType,
              message: i18n._(
                plural("value_error.thread_title.max_length", {
                  value: max,
                  one: `Thread title should be no longer than # character (it has ${value}).`,
                  other: `Thread title should be no longer than # characters (it has ${value}).`,
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

export default ThreadTitleValidationError
