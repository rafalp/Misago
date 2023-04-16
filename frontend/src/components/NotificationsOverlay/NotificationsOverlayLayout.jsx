import classnames from "classnames"
import React from "react"
import { DropdownFooter, DropdownHeader, DropdownPills } from "../Dropdown"

export default function NotificationsOverlayLayout({
  children,
  close,
  showAll,
  showUnread,
  unread,
}) {
  return (
    <div className="notifications-overlay-layout">
      <div className="notifications-overlay-header">
        <div className="notifications-overlay-caption">
          {pgettext("notifications title", "Notifications")}
        </div>
        <button
          className="btn btn-notifications-overlay"
          title={pgettext("dialog", "Cancel")}
          type="button"
          onClick={close}
        >
          <span className="material-icon">close</span>
        </button>
      </div>
      <DropdownPills>
        <NotificationsOverlayLayoutPill active={!unread} onClick={showAll}>
          {pgettext("notifications dropdown", "All")}
        </NotificationsOverlayLayoutPill>
        <NotificationsOverlayLayoutPill active={unread} onClick={showUnread}>
          {pgettext("notifications dropdown", "Unread")}
        </NotificationsOverlayLayoutPill>
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

function NotificationsOverlayLayoutPill({ active, children, onClick }) {
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
