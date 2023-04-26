import classnames from "classnames"
import React from "react"
import { DropdownFooter, DropdownPills } from "../Dropdown"
import { Overlay, OverlayHeader } from "../Overlay"

export default function NotificationsOverlayBody({
  children,
  close,
  showAll,
  showUnread,
  unread,
}) {
  return (
    <div className="notifications-overlay-body">
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
        <NotificationsOverlayBodyPill active={!unread} onClick={showAll}>
          {pgettext("notifications dropdown", "All")}
        </NotificationsOverlayBodyPill>
        <NotificationsOverlayBodyPill active={unread} onClick={showUnread}>
          {pgettext("notifications dropdown", "Unread")}
        </NotificationsOverlayBodyPill>
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

function NotificationsOverlayBodyPill({ active, children, onClick }) {
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
