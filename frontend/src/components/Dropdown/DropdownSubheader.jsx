import classnames from "classnames"
import React from "react"

export default function DropdownSubheader({ className, children }) {
  return (
    <li className={classnames("dropdown-subheader", className)}>{children}</li>
  )
}
