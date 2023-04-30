import classnames from "classnames"
import React from "react"
import Avatar from "../avatar"

export default function NavbarUserNavToggle({
  id,
  className,
  user,
  active,
  onClick,
}) {
  return (
    <a
      id={id}
      className={classnames("btn-navbar-image", className, { active })}
      href={user.url}
      title={pgettext("navbar", "Open your options")}
      onClick={onClick}
    >
      <Avatar user={user} size={34} />
    </a>
  )
}
