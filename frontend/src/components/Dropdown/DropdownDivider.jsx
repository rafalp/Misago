import classnames from "classnames"
import React from "react"

export default function DropdownDivider({ className }) {
  return <li className={classnames("divider", className)}></li>
}
