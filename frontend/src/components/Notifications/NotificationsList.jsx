import React from "react"
import NotificationsListItem from "./NotificationsListItem"

export default function NotificationsList({ items, hasNext, hasPrevious }) {
  return (
    <div className="notifications-list">
      <ul className="list-group">
        {items.map((notification) => (
          <NotificationsListItem
            key={notification.id}
            notification={notification}
          />
        ))}
      </ul>
    </div>
  )
}
