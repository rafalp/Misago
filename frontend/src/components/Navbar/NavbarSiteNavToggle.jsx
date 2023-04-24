import classnames from "classnames"
import React from "react"

export default function NavbarSiteNavToggle({
  id,
  className,
  active,
  onClick,
}) {
  return (
    <button
      id={id}
      className={classnames("btn btn-navbar-icon", className, { active })}
      title={pgettext("navbar", "Open menu")}
      type="button"
      onClick={onClick}
    >
      <span className="material-icon">menu</span>
    </button>
  )
}
