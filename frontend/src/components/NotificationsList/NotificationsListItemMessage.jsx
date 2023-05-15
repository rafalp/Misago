import classnames from "classnames"
import React from "react"

export default function NotificationsListItemMessage({ notification }) {
  return (
    <a
      href={notification.url}
      className={classnames("notification-message", {
        "notification-message-read": notification.isRead,
        "notification-message-unread": !notification.isRead,
      })}
      dangerouslySetInnerHTML={{ __html: notification.message }}
    />
  )
}
