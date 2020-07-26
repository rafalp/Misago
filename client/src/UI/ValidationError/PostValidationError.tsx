import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import ValidationError from "./ValidationError"
import { IValidationErrorProps } from "./ValidationError.types"

const ERROR_TYPES_MAP: Record<string, string> = {
  required: "value_error.missing",
}

const PostValidationError: React.FC<IValidationErrorProps> = ({
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
          case "auth_error.not_moderator":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "auth_error.not_moderator.post"
                )`You can't moderate this post.`
              ),
            })

          case "auth_error.category.closed":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "auth_error.post_category.closed"
                )`This post's category is closed.`
              ),
            })

          case "auth_error.thread.closed":
            return children({
              type: errorType,
              message: i18n._(
                t("auth_error.thread.closed")`This post's thread is closed.`
              ),
            })

          case "auth_error.post.not_author":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "auth_error.post.not_author"
                )`You need to be this post's author to perform this action.`
              ),
            })

          case "value_error.post.thread_start":
            return children({
              type: errorType,
              message: i18n._(
                t(
                  "value_error.post.thread_start"
                )`This post is thread's original post. It can't be moved or deleted.`
              ),
            })

          case "value_error.post.not_exists":
            return children({
              type: errorType,
              message: i18n._(
                t("value_error.post.not_exists")`Post could not be found.`
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

export default PostValidationError
