import classnames from "classnames"
import React from "react"
import { Link } from "react-router"

export default function PillsNavLink({ active, link, icon, children }) {
  return (
    <li className={classnames({ active })}>
      <Link to={link} activeClassName="">
        {!!icon && <span className="material-icon">{icon}</span>}
        {children}
      </Link>
    </li>
  )
}
