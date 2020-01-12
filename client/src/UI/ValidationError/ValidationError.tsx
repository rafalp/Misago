import { plural, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { IValidationErrorProps } from "./ValidationError.types"

const ValidationError: React.FC<IValidationErrorProps> = ({ children, error, messages, value=0, min=0, max=0 }) => {
  if (!error) return null
  if (messages && messages[error]) {
    return children({ type: error, message: messages[error] })
  }

  return (
    <I18n>
      {({ i18n }) => {
        switch (error) {
          case "value_error.missing":
            return children({
              type: error,
              message: i18n._(t("value_error.missing")`This field can't be empty.`),
            })

          case "value_error.any_str.min_length":
            return children({
              type: error,
              message: i18n._(plural("value_error.any_str.min_length", {
                value: min,
                one: `This value should be at least # character long (it has ${value}).`,
                other: `This value should be at least # characters long (it has ${value}).`,
              })),
            })

            case "value_error.any_str.max_length":
              return children({
                type: error,
                message: i18n._(plural("value_error.any_str.max_length", {
                  value: max,
                  one: `This value should be no longer than # character (it has ${value}).`,
                  other: `This value should be no longer than # characters (it has ${value}).`,
                })),
              })

          default:
            return children({ type: error, message: error })
        }
      }}
    </I18n>
  )
}

export default ValidationError
