import classnames from "classnames"
import React from "react"

const PageHeader = ({ children, className, styleName }) => (
  <div
    className={classnames(
      "page-header",
      className,
      styleName && "page-header-" + styleName
    )}
  >
    <div className="page-header-bg-image">
      <div className="page-header-bg-overlay">
        <div className="page-header-image" />
        {children}
      </div>
    </div>
  </div>
)

export default PageHeader
