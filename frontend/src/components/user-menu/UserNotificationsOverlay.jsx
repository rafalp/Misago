import React from "react"
import { connect } from "react-redux"
import { open } from "../../reducers/notifications"

function UserNotificationsOverlay({ dispatch, user }) {
  let title = null
  if (user.unreadNotifications) {
    title = gettext("You have unread notifications!")
  } else {
    title = pgettext("navbar link", "Notifications")
  }

  return (
    <li>
      <a
        className="navbar-icon"
        href={misago.get("NOTIFICATIONS_URL")}
        onClick={(event) => {
          event.preventDefault()
          dispatch(open())
        }}
        title={title}
      >
        <span className="material-icon">
          {!!user.unreadNotifications
            ? "notifications_active"
            : "notifications_none"}
        </span>
        {!!user.unreadNotifications && (
          <span className="badge">{user.unreadNotifications}</span>
        )}
      </a>
    </li>
  )
}

const UserNotificationsOverlayConnected = connect()(UserNotificationsOverlay)

export default UserNotificationsOverlayConnected
