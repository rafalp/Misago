import classnames from "classnames"
import React from "react"

const ToolbarSection = ({ children, className }) => (
  <div className={classnames("toolbar-section", className)}>{children}</div>
)

export default ToolbarSection