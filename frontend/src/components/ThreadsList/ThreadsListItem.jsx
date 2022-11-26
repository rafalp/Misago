import React from "react"
import Avatar from "../avatar"
import ThreadsListItemActivity from "./ThreadsListItemActivity"
import ThreadsListItemCategory from "./ThreadsListItemCategory"
import ThreadsListItemIcon from "./ThreadListItemIcon"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"
import ThreadsListItemReplies from "./ThreadsListItemReplies"

const ThreadsListItem = ({ activeCategory, categories, thread }) => {
  let category = null
  if (activeCategory.id !== thread.category) {
    category = categories[thread.category]
  }
  console.log(category)

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
      {!!category && (
        <div className="threads-list-item-col-category">
          <ThreadsListItemCategory category={category} />
        </div>
      )}
      <div className="threads-list-item-col-replies">
        <ThreadsListItemReplies thread={thread} />
      </div>
      <div className="threads-list-item-col-last-poster">
        <ThreadsListItemLastPoster thread={thread} />
      </div>
      <div className="threads-list-item-col-last-activity">
        <ThreadsListItemActivity thread={thread} />
      </div>
    </li>
  )
}

export default ThreadsListItem