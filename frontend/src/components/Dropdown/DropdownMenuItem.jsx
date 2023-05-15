import classnames from "classnames"
import React from "react"

export default function DropdownMenuItem({ className, children }) {
  return (
    <li className={classnames("dropdown-menu-item", className)}>{children}</li>
  )
}
