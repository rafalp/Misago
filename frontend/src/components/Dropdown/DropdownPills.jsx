import classnames from "classnames"
import React from "react"

export default function DropdownPills({ className, children }) {
  return (
    <div className={classnames("dropdown-pills", className)}>{children}</div>
  )
}
