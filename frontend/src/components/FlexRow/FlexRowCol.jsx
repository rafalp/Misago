import classnames from "classnames"
import React from "react"

const FlexRowCol = ({ children, className, shrink }) => (
  <div
    className={classnames("flex-row-col", className, {
      "flex-row-col-shrink": shrink,
    })}
  >
    {children}
  </div>
)

export default FlexRowCol
