import React from "react"
import { Dropdown } from "../Dropdown"
import NotificationsDropdown from "../NotificationsDropdown"

export default function UserNotifications({ user }) {
  let title = null
  if (user.unreadNotifications) {
    title = gettext("You have unread notifications!")
  } else {
    title = pgettext("navbar link", "Notifications")
  }

  return (
    <Dropdown
      toggle={({ aria, toggle }) => (
        <a
          {...aria}
          className="navbar-icon"
          href={misago.get("NOTIFICATIONS_URL")}
          onClick={(event) => {
            event.preventDefault()
            toggle()
          }}
          title={title}
        >
          <span className="material-icon">
            {user.unreadNotifications
              ? "notifications_active"
              : "notifications_none"}
          </span>
          {!!user.unreadNotifications && (
            <span className="badge">
              {user.unreadNotifications > 50 ? "50+" : user.unreadNotifications}
            </span>
          )}
        </a>
      )}
      listItem
      menuClassName="notifications-dropdown"
      menuRightAlign
    >
      {({ isOpen }) => <NotificationsDropdown disabled={!isOpen} />}
    </Dropdown>
  )
}
