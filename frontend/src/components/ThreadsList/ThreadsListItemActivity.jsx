import React from "react"

const ThreadsListItemActivity = ({ thread }) => (
  <a
    href={thread.url.last_post}
    className="threads-list-item-last-activity"
    title={interpolate(
      gettext("Last activity: %(timestamp)s"),
      {
        timestamp: thread.last_post_on.format("LLL"),
      },
      true
    )}
  >
    {thread.last_post_on.fromNow(true)}
  </a>
)

export default ThreadsListItemActivity