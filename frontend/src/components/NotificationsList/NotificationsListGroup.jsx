import classnames from "classnames"
import React from "react"
import { ListGroup } from "../ListGroup"

export default function NotificationsListGroup({ className, children }) {
  return (
    <div className={classnames("notifications-list", className)}>
      <ListGroup>{children}</ListGroup>
    </div>
  )
}
