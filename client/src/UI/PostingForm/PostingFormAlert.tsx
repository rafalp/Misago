import classnames from "classnames"
import React from "react"

interface IPostingFormAlertProps {
  appearance?:
    | "primary"
    | "secondary"
    | "success"
    | "danger"
    | "warning"
    | "info"
  className?: string
  children: React.ReactNode
}

const PostingFormAlert: React.FC<IPostingFormAlertProps> = ({
  appearance = "danger",
  children,
  className,
}) => (
  <div
    className={classnames(
      "posting-form-alert",
      `posting-form-alert-${appearance}`,
      className
    )}
  >
    <div
      className={classnames(
        "alert",
        "alert-responsive",
        `alert-${appearance}`,
        className
      )}
      role="alert"
    >
      {children}
    </div>
  </div>
)

export default PostingFormAlert
