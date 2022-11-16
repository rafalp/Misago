import React from "react"
import ThreadsListItemIcon from "./ThreadListItemIcon"

const ThreadsListItem = ({ thread }) => {
  return (
    <li className="list-group-item threads-list-item">
      <div className="threads-list-item-col-icon">
        <ThreadsListItemIcon thread={thread} />
      </div>
      <div className="threads-list-item-col-title">
        <a
          href={thread.is_read ? thread.url.index : thread.url.new_post}
          className={"item-title threads-list-item-title" + (!thread.is_read ? " threads-list-item-title-new" : "")}
        >
          {thread.title}
        </a>
      </div>
      <div className="threads-list-item-col-last-activity">
        <a
          href={thread.url.last_post}
          className="threads-list-item-last-activity"
          title={gettext("Last activity:") + " " + thread.last_post_on.format("LLL")}
        >
          {thread.last_post_on.fromNow(true)}
        </a>
      </div>
    </li>
  )
}

export default ThreadsListItem