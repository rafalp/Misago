import React from "react"
import NotificationsListGroup from "./NotificationsListGroup"

export default function NotificationsListLoading() {
  return (
    <NotificationsListGroup className="notifications-list-pending">
      <li className="list-group-item notifications-list-loading">
        <p className="notifications-list-loading-message">
          {pgettext("notifications list", "Loading notifications...")}
        </p>
        <div className="notifications-list-loading-progress">
          <div className="notifications-list-loading-progress-bar"></div>
        </div>
      </li>
    </NotificationsListGroup>
  )
}
