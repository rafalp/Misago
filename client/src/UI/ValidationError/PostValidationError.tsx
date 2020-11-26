import { t } from "@lingui/macro"
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

  switch (errorType) {
    case "auth_error.not_moderator":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.not_moderator.post",
          message: "You can't moderate this post.",
        }),
      })

    case "auth_error.category.closed":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.post_category.closed",
          message: "This post's category is closed.",
        }),
      })

    case "auth_error.thread.closed":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.thread.closed",
          message: "This post's thread is closed.",
        }),
      })

    case "auth_error.post.not_author":
      return children({
        type: errorType,
        message: t({
          id: "auth_error.post.not_author",
          message: "You need to be this post's author to perform this action.",
        }),
      })

    case "value_error.post.thread_start":
      return children({
        type: errorType,
        message: t({
          id: "value_error.post.thread_start",
          message: "This post is thread's original post.",
        }),
      })

    case "value_error.post.not_exists":
      return children({
        type: errorType,
        message: t({
          id: "value_error.post.not_exists",
          message: "Post could not be found.",
        }),
      })
  }

  return (
    <ValidationError error={error} value={value} min={min} max={max}>
      {children}
    </ValidationError>
  )
}

export default PostValidationError
