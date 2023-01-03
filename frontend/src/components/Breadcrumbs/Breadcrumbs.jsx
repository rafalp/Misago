import classnames from "classnames"
import React from "react"

const Breadcrumbs = ({ children, className }) => (
  <ul className={classnames("breadcrumbs", className)}>{children}</ul>
)

export default Breadcrumbs
