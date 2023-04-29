import classnames from "classnames"
import React from "react"

export default function ListGroupItem({ className, children }) {
  return (
    <li className={classnames("list-group-item", className)}>{children}</li>
  )
}
