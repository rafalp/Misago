import React from "react"
import NotificationsListGroup from "./NotificationsListGroup"

export default function NotificationsListError({ error }) {
  console.log(error)

  const detail = errorDetail(error)

  return (
    <NotificationsListGroup className="notifications-list-pending">
      <li className="list-group-item notifications-list-error">
        <div className="notifications-list-error-icon">
          <span className="material-icon">notifications_off</span>
        </div>
        <p className="notifications-list-error-message">
          {pgettext("notifications list", "Notifications could not be loaded.")}
        </p>
        {!!detail && (
          <p className="notifications-list-error-detail">{detail}</p>
        )}
      </li>
    </NotificationsListGroup>
  )
}

function errorDetail(error) {
  if (error.status === 0) {
    return pgettext(
      "notifications list",
      "Site could not be reached. Check your internet connection and try refreshing the site."
    )
  }

  if (error.data && error.data.detail) {
    return error.data.detail
  }
}
