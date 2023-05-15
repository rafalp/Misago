import classnames from "classnames"
import React from "react"

export default function DropdownHeader({ className, children }) {
  return (
    <div className={classnames("dropdown-header", className)}>{children}</div>
  )
}
