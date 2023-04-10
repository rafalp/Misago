import React from "react"
import NotificationsDropdownItem from "./NotificationsDropdownItem"

export default function NotificationsDropdownList({ items }) {
  return (
    <div className="notifications-dropdown-list">
      {items.map((notification) => (
        <NotificationsDropdownItem
          key={notification.id}
          notification={notification}
        />
      ))}
    </div>
  )
}
