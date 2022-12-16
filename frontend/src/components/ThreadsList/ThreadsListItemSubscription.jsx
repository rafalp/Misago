import React from "react"
import ThreadsListItemSubscriptionOptions from "./ThreadsListItemSubscriptionOptions"

const ThreadsListItemSubscription = ({ disabled, thread }) => (
  <div className="dropdown">
    <button
      className="btn btn-default btn-icon"
      type="button"
      title={getSubscriptionTitle(thread.subscription)}
      disabled={disabled}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
    >
      <span className="material-icon">
        {getSubscriptionIcon(thread.subscription)}
      </span>
    </button>
    <ThreadsListItemSubscriptionOptions
      disabled={disabled}
      thread={thread}
    />
  </div>
)

const getSubscriptionTitle = (subscription) => {
  if (subscription === true) return gettext("Subscribed to e-mails")
  if (subscription === false) return gettext("Subscribed to alerts")
  return gettext("Not subscribed")
}

const getSubscriptionIcon = (subscription) => {
  if (subscription === true) return "star"
  if (subscription === false) return "star_half"
  return "star_border"
}

export default ThreadsListItemSubscription
