import React from "react"
import { ListGroupEmpty } from "../ListGroup"

export default function NotificationsListEmpty({ filter }) {
  return (
    <ListGroupEmpty
      icon={
        filter === "unread" ? "sentiment_very_satisfied" : "notifications_none"
      }
      message={emptyMessage(filter)}
    />
  )
}

function emptyMessage(filter) {
  if (filter === "read") {
    return pgettext(
      "notifications list",
      "You don't have any read notifications."
    )
  } else if (filter === "unread") {
    return pgettext(
      "notifications list",
      "You don't have any unread notifications."
    )
  }

  return pgettext("notifications list", "You don't have any notifications.")
}
