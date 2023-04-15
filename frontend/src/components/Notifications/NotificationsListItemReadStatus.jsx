import React from "react"

export default function NotificationsListItemReadStatus({ notification }) {
  if (notification.isRead) {
    return (
      <div
        className="notifications-list-item-read-status"
        title={pgettext("notification status", "Read notification")}
      >
        <span className="notification-read-icon"></span>
      </div>
    )
  }

  return (
    <div
      className="notifications-list-item-read-status"
      title={pgettext("notification status", "Unread notification")}
    >
      <span className="notification-unread-icon"></span>
    </div>
  )
}
