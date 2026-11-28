import classnames from "classnames"
import React from "react"

export default function NavbarSearch({
  id,
  className,
  showQuickSearch,
  url,
  active,
}) {
  return (
    <a
      id={id}
      className={classnames("btn btn-navbar-icon", className, { active })}
      href={url}
      title={pgettext("navbar", "Open search")}
      {...(showQuickSearch && {
        "data-toggle": "modal",
        "data-target": "#quick-search",
        "data-remote": "false",
      })}
    >
      <span className="material-icon">search</span>
    </a>
  )
}
