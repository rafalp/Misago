import classnames from "classnames"
import React from "react"

export default function NotificationsListGroup({ className, children }) {
  return (
    <div className={classnames("notifications-list", className)}>
      <ul className="list-group">{children}</ul>
    </div>
  )
}
