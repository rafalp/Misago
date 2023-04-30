import classnames from "classnames"
import React from "react"

export default function NavbarSearchToggle({
  id,
  className,
  url,
  active,
  onClick,
}) {
  return (
    <a
      id={id}
      className={classnames("btn btn-navbar-icon", className, { active })}
      href={url}
      title={pgettext("navbar", "Open search")}
      onClick={onClick}
    >
      <span className="material-icon">search</span>
    </a>
  )
}
