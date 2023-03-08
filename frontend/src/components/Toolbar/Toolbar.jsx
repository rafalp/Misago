import classnames from "classnames"
import React from "react"

const Toolbar = ({ children, className }) => (
  <nav className={classnames("toolbar", className)}>{children}</nav>
)

export default Toolbar
