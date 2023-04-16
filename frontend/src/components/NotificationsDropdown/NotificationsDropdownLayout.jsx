import classnames from "classnames"
import React from "react"
import { DropdownFooter, DropdownHeader, DropdownPills } from "../Dropdown"

export default function NotificationsDropdownLayout({
  children,
  showAll,
  showUnread,
  unread,
}) {
  return (
    <div className="notifications-dropdown-layout">
      <DropdownHeader>
        {pgettext("notifications title", "Notifications")}
      </DropdownHeader>
      <DropdownPills>
        <NotificationsDropdownLayoutPill active={!unread} onClick={showAll}>
          {pgettext("notifications dropdown", "All")}
        </NotificationsDropdownLayoutPill>
        <NotificationsDropdownLayoutPill active={unread} onClick={showUnread}>
          {pgettext("notifications dropdown", "Unread")}
        </NotificationsDropdownLayoutPill>
      </DropdownPills>
      {children}
      <DropdownFooter>
        <a
          className="btn btn-default btn-block"
          href={misago.get("NOTIFICATIONS_URL")}
        >
          {pgettext("notifications", "See all notifications")}
        </a>
      </DropdownFooter>
    </div>
  )
}

function NotificationsDropdownLayoutPill({ active, children, onClick }) {
  return (
    <button
      className={classnames("btn", {
        "btn-primary": active,
        "btn-default": !active,
      })}
      type="button"
      onClick={onClick}
    >
      {children}
    </button>
  )
}
