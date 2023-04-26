import classnames from "classnames"
import React from "react"
import { DropdownFooter, DropdownHeader, DropdownPills } from "../Dropdown"

export default function NotificationsDropdownBody({
  children,
  showAll,
  showUnread,
  unread,
}) {
  return (
    <div className="notifications-dropdown-body">
      <DropdownHeader>
        {pgettext("notifications title", "Notifications")}
      </DropdownHeader>
      <DropdownPills>
        <NotificationsDropdownBodyPill active={!unread} onClick={showAll}>
          {pgettext("notifications dropdown", "All")}
        </NotificationsDropdownBodyPill>
        <NotificationsDropdownBodyPill active={unread} onClick={showUnread}>
          {pgettext("notifications dropdown", "Unread")}
        </NotificationsDropdownBodyPill>
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

function NotificationsDropdownBodyPill({ active, children, onClick }) {
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
