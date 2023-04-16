import classnames from "classnames"
import React from "react"
import NotificationsListItemActor from "./NotificationsListItemActor"
import NotificationsListItemMessage from "./NotificationsListItemMessage"
import NotificationsListItemReadStatus from "./NotificationsListItemReadStatus"
import NotificationsListItemTimestamp from "./NotificationsListItemTimestamp"

export default function NotificationsListItem({ notification }) {
  return (
    <li
      key={notification.id}
      className={classnames("list-group-item notifications-list-item", {
        "notifications-list-item-read": notification.isRead,
        "notifications-list-item-unread": !notification.isRead,
      })}
    >
      <div className="notifications-list-item-left-col">
        <div className="notifications-list-item-col-actor">
          <NotificationsListItemActor notification={notification} />
        </div>
        <div className="notifications-list-item-col-read-icon">
          <NotificationsListItemReadStatus notification={notification} />
        </div>
      </div>
      <div className="notifications-list-item-right-col">
        <div className="notifications-list-item-col-message">
          <NotificationsListItemMessage notification={notification} />
        </div>
        <div className="notifications-list-item-col-timestamp">
          <NotificationsListItemTimestamp notification={notification} />
        </div>
      </div>
    </li>
  )
}
