import React from "react"
import { Link } from "react-router"

export default function NotificationsPagination({ baseUrl, data, disabled }) {
  return (
    <div className="misago-pagination">
      <NotificationsPaginationLink
        url={baseUrl}
        disabled={disabled || !data || !data.hasPrevious}
      >
        {pgettext("notifications pagination", "Latest")}
      </NotificationsPaginationLink>
      <NotificationsPaginationLink
        url={baseUrl + "?before=" + (data ? data.firstCursor : "")}
        disabled={disabled || !data || !data.hasPrevious}
      >
        {pgettext("notifications pagination", "Newer")}
      </NotificationsPaginationLink>
      <NotificationsPaginationLink
        url={baseUrl + "?after=" + (data ? data.lastCursor : "")}
        disabled={disabled || !data || !data.hasNext}
      >
        {pgettext("notifications pagination", "Older")}
      </NotificationsPaginationLink>
    </div>
  )
}

function NotificationsPaginationLink({ disabled, children, url }) {
  if (disabled) {
    return (
      <button className="btn btn-default" type="disabled" disabled>
        {children}
      </button>
    )
  }

  return (
    <Link to={url} className="btn btn-default" activeClassName="">
      {children}
    </Link>
  )
}
