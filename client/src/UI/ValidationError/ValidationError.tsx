import { plural, t } from "@lingui/macro"
import React from "react"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
  min: "value_error.any_str.min_length",
  max: "value_error.any_str.max_length",
}

const ValidationError: React.FC<IValidationErrorProps> = ({
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
          id: "auth_error.not_moderator",
          message: "You need to be a moderator to perform this action.",
        }),
      })

    case "value_error.missing":
      return children({
        type: errorType,
        message: t({
          id: "value_error.missing",
          message: "This field can't be empty.",
        }),
      })

    case "value_error.any_str.min_length":
      return children({
        type: errorType,
        message: t({
          id: "value_error.any_str.min_length",
          message: plural(min, {
            one: `This value should be at least # character long (it has ${value}).`,
            other: `This value should be at least # characters long (it has ${value}).`,
          }),
        }),
      })

    case "value_error.any_str.max_length":
      return children({
        type: errorType,
        message: t({
          id: "value_error.any_str.max_length",
          message: plural(max, {
            one: `This value should be no longer than # character (it has ${value}).`,
            other: `This value should be no longer than # characters (it has ${value}).`,
          }),
        }),
      })
  }

  return children(error)
}

export default ValidationError
