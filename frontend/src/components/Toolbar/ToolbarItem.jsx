import classnames from "classnames"
import React from "react"

const ToolbarItem = ({ children, className, shrink }) => (
  <div
    className={classnames("toolbar-item", className, {
      "toolbar-item-shrink": shrink,
    })}
  >
    {children}
  </div>
)

export default ToolbarItem
