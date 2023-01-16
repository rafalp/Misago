import classnames from "classnames"
import React from "react"

const FlexRow = ({ children, className }) => (
  <div className={classnames("flex-row", className)}>{children}</div>
)

export default FlexRow
