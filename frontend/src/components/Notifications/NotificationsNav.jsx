import classnames from "classnames"
import React from "react"
import { Link } from "react-router"

export default function NotificationsNav({ filter }) {
  const basename = misago.get("NOTIFICATIONS_URL")

  return (
    <div className="nav nav-pills">
      <li className={classnames({ active: filter === "all" })}>
        <Link to={basename} activeClassName="">
          {pgettext("notifications nav", "All")}
        </Link>
      </li>
      <li className={classnames({ active: filter === "unread" })}>
        <Link to={basename + "unread/"} activeClassName="">
          {pgettext("notifications nav", "Unread")}
        </Link>
      </li>
      <li className={classnames({ active: filter === "read" })}>
        <Link to={basename + "read/"} activeClassName="">
          {pgettext("notifications nav", "Read")}
        </Link>
      </li>
    </div>
  )
}
