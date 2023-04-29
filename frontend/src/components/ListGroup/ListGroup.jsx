import classnames from "classnames"
import React from "react"

export default function ListGroup({ className, children }) {
  return <ul className={classnames("list-group", className)}>{children}</ul>
}
