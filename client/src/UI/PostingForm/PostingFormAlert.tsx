import classnames from "classnames"
import React from "react"

interface IPostingFormAlertProps {
  className?: string
  children: React.ReactNode
}

const PostingFormAlert: React.FC<IPostingFormAlertProps> = ({
  children,
  className,
}) => (
  <div className={classnames("posting-form-alert", className)}>
    <div
      className="alert alert-responsive alert-danger"
      role="alert"
    >
      {children}
    </div>
  </div>
)

export default PostingFormAlert
