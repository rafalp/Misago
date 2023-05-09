import React from "react"
import ThreadsListItemNotificationsOptions from "./ThreadsListItemNotificationsOptions"

const ThreadsListItemNotifications = ({ disabled, thread }) => (
  <div className="dropdown">
    <button
      className="btn btn-default btn-icon"
      type="button"
      title={getTitle(thread.notifications)}
      disabled={disabled}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <span className="material-icon">
        {getIcon(thread.notifications)}
      </span>
    </button>
    <ThreadsListItemNotificationsOptions disabled={disabled} thread={thread} />
  </div>
)

const getIcon = (notifications) => {
  if (notifications === 2) return "mail"
  if (notifications === 1) return "notifications_active"

  return "notifications_none"
}

const getTitle = (notifications) => {
  if (notifications === 2) {
    return pgettext("watch thread", "Send e-mail notifications")
  }

  if (notifications === 1) {
    return pgettext("watch thread", "Without e-mail notifications")
  }

  return gettext("Not watching")
}

export default ThreadsListItemNotifications
