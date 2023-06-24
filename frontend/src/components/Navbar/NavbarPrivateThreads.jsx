import classnames from "classnames"
import React from "react"

export default function NavbarPrivateThreads({
  id,
  className,
  badge,
  url,
  active,
  onClick,
}) {
  const title = !!badge
    ? pgettext("navbar", "You have unread private threads!")
    : pgettext("navbar", "Open private threads")

  return (
    <a
      id={id}
      className={classnames("btn btn-navbar-icon", className, { active })}
      href={url}
      title={title}
      onClick={onClick}
    >
      {!!badge && <span className="navbar-item-badge">{badge}</span>}
      <span className="material-icon">inbox</span>
    </a>
  )
}
