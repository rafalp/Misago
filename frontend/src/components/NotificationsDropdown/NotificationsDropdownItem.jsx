import React from "react"

export default function NotificationsDropdownItem({ notification }) {
  return <div dangerouslySetInnerHTML={{ __html: notification.message }} />
}
