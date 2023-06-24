import classnames from "classnames"
import React from "react"

export default function NavbarNotificationsToggle({
  id,
  className,
  badge,
  url,
  active,
  onClick,
}) {
  const title = !!badge
    ? pgettext("navbar", "You have unread notifications!")
    : pgettext("navbar", "Open notifications")

  return (
    <a
      id={id}
      className={classnames("btn btn-navbar-icon", className, { active })}
      href={url}
      title={title}
      onClick={onClick}
    >
      {!!badge && <span className="navbar-item-badge">{badge}</span>}
      <span className="material-icon">
        {!!badge ? "notifications_active" : "notifications_none"}
      </span>
    </a>
  )
}
