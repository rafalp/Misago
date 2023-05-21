import React from "react"
import Timestamp from "../Timestamp"

const ThreadsListItemActivity = ({ thread }) => (
  <a href={thread.url.last_post} className="threads-list-item-last-activity">
    <Timestamp
      datetime={thread.last_post_on}
      title={pgettext("threads list", "%(timestamp)s - latest activity")}
      narrow
    />
  </a>
)

export default ThreadsListItemActivity
