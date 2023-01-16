import classnames from "classnames"
import React from "react"

const PageHeaderBanner = ({ children, className, styleName }) => (
  <div
    className={classnames(
      "page-header-banner",
      className,
      styleName && "page-header-banner-" + styleName
    )}
  >
    <div className="page-header-banner-bg-image">
      <div className="page-header-banner-bg-overlay">{children}</div>
    </div>
  </div>
)

export default PageHeaderBanner
