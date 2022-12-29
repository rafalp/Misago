import classnames from "classnames"
import React from "react"

const PageHeaderMessage = ({ children, className }) => (
  <div className={classnames("page-header-message", className)}>{children}</div>
)

export default PageHeaderMessage
