import classnames from "classnames"
import React from "react"
import { DropdownFooter, DropdownPills } from "../Dropdown"
import { Overlay, OverlayHeader } from "../Overlay"

export default function NotificationsOverlayBody({
  children,
  open,
  showAll,
  showUnread,
  unread,
}) {
  return (
    <Overlay open={open}>
      <OverlayHeader>
        {pgettext("notifications title", "Notifications")}
      </OverlayHeader>
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
    </Overlay>
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
