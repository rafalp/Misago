import classnames from "classnames"
import React from "react"

const PageHeaderHTMLMessage = ({ className, message }) => (
  <div
    className={classnames("page-header-message", className)}
    dangerouslySetInnerHTML={{ __html: message }}
  />
)

export default PageHeaderHTMLMessage
