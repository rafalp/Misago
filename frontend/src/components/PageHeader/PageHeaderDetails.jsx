import classnames from "classnames"
import React from "react"

const PageHeaderDetails = ({ children, className }) => (
  <div className={classnames("page-header-details", className)}>{children}</div>
)

export default PageHeaderDetails
