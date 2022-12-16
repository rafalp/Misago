import React from "react"
import ThreadsListItemActivity from "./ThreadsListItemActivity"
import ThreadsListItemCategory from "./ThreadsListItemCategory"
import ThreadsListItemCheckbox from "./ThreadsListItemCheckbox"
import ThreadsListItemFlags from "./ThreadsListItemFlags"
import ThreadsListItemIcon from "./ThreadsListItemIcon"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"
import ThreadsListItemReplies from "./ThreadsListItemReplies"
import ThreadsListItemSubscription from "./ThreadsListItemSubscription"

const ThreadsListItem = ({
  activeCategory,
  categories,
  showOptions,
  thread,
  isBusy,
  isSelected,
}) => {
  let category = null
  if (activeCategory.id !== thread.category) {
    category = categories[thread.category]
  }

  const hasFlags = (
    thread.is_closed ||
    thread.is_hidden ||
    thread.is_unapproved ||
    thread.weight > 0 ||
    thread.best_answer ||
    thread.has_poll ||
    thread.has_unapproved_posts
  )

  const isNew = showOptions ? thread.is_new : true

  return (
    <li className="list-group-item threads-list-item">
      {showOptions && (
        <div className="threads-list-item-col-icon">
          <ThreadsListItemIcon thread={thread} />
        </div>
      )}
      <div className="threads-list-item-col-title">
        <a
          href={isNew ? thread.url.new_post : thread.url.index}
          className={"threads-list-item-title" + (isNew ? " threads-list-item-title-new" : "")}
        >
          {thread.title}
        </a>
      </div>
      {hasFlags && (
        <div className="threads-list-item-col-flags">
          <ThreadsListItemFlags thread={thread} />
        </div>
      )}
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
      {showOptions && (
        <div className="threads-list-item-col-subscription">
          <ThreadsListItemSubscription
            disabled={isBusy}
            thread={thread}
          />
        </div>
      )}
      {(showOptions && thread.moderation.length > 0) && (
        <div className="threads-list-item-col-checkbox">
          <ThreadsListItemCheckbox
            checked={isSelected}
            disabled={isBusy}
            thread={thread}
          />
        </div>
      )}
    </li>
  )
}

export default ThreadsListItem