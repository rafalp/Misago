import React from "react"

export default function NotificationsDropdownEmpty({ unread }) {
  return (
    <div className="notifications-dropdown-empty">
      {unread ? "No unread" : "No read"}
    </div>
  )
}
