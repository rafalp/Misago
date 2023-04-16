import React from "react"
import NotificationsListEmpty from "./NotificationsListEmpty"
import NotificationsListGroup from "./NotificationsListGroup"
import NotificationsListItem from "./NotificationsListItem"

export default function NotificationsList({ filter, items }) {
  return (
    <NotificationsListGroup
      className={
        items.length > 0
          ? "notifications-list-ready"
          : "notifications-list-pending"
      }
    >
      {items.length === 0 && <NotificationsListEmpty filter={filter} />}
      {items.map((notification) => (
        <NotificationsListItem
          key={notification.id}
          notification={notification}
        />
      ))}
    </NotificationsListGroup>
  )
}
