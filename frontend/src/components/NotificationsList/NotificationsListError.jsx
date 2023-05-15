import React from "react"
import { ListGroupError } from "../ListGroup"
import NotificationsListGroup from "./NotificationsListGroup"

export default function NotificationsListError({ error }) {
  const detail = errorDetail(error)

  return (
    <NotificationsListGroup className="notifications-list-pending">
      <ListGroupError
        icon="notifications_off"
        message={pgettext(
          "notifications list",
          "Notifications could not be loaded."
        )}
        detail={detail}
      />
    </NotificationsListGroup>
  )
}

function errorDetail(error) {
  if (error.status === 0) {
    return gettext(
      "Check your internet connection and try refreshing the site."
    )
  }

  if (error.data && error.data.detail) {
    return error.data.detail
  }
}
