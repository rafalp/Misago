import { plural, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  "required": "value_error.missing",
  "min": "value_error.any_str.min_length",
  "max": "value_error.any_str.max_length",
}

const ValidationError: React.FC<IValidationErrorProps> = ({ children, error, messages, value=0, min=0, max=0 }) => {
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
              message: i18n._(t("value_error.missing")`This field can't be empty.`),
            })

          case "value_error.any_str.min_length":
            return children({
              type: errorType,
              message: i18n._(plural("value_error.any_str.min_length", {
                value: min,
                one: `This value should be at least # character long (it has ${value}).`,
                other: `This value should be at least # characters long (it has ${value}).`,
              })),
            })

            case "value_error.any_str.max_length":
              return children({
                type: errorType,
                message: i18n._(plural("value_error.any_str.max_length", {
                  value: max,
                  one: `This value should be no longer than # character (it has ${value}).`,
                  other: `This value should be no longer than # characters (it has ${value}).`,
                })),
              })

          default:
            return children(error)
        }
      }}
    </I18n>
  )
}

export default ValidationError
