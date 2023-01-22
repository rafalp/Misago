import React from "react"
import ThreadFlags from "../ThreadFlags"
import ThreadReplies from "../ThreadReplies"
import ThreadsListItemActivity from "./ThreadsListItemActivity"
import ThreadsListItemCategory from "./ThreadsListItemCategory"
import ThreadsListItemCheckbox from "./ThreadsListItemCheckbox"
import ThreadsListItemIcon from "./ThreadsListItemIcon"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"
import ThreadsListItemSubscription from "./ThreadsListItemSubscription"

const ThreadsListItem = ({
  activeCategory,
  categories,
  showOptions,
  showSubscription,
  thread,
  isBusy,
  isSelected,
}) => {
  let parent = null
  let category = null

  if (activeCategory.id !== thread.category) {
    category = categories[thread.category]

    if (
      category.parent &&
      category.parent !== activeCategory.id &&
      categories[category.parent] &&
      !categories[category.parent].special_role
    ) {
      parent = categories[category.parent]
    }
  }

  const hasFlags =
    thread.is_closed ||
    thread.is_hidden ||
    thread.is_unapproved ||
    thread.weight > 0 ||
    thread.best_answer ||
    thread.has_poll ||
    thread.has_unapproved_posts

  const isNew = showOptions ? thread.is_new : true

  return (
    <li
      className={
        "list-group-item threads-list-item" +
        (isBusy ? " threads-list-item-is-busy" : "")
      }
    >
      <div className="threads-list-item-top-row">
        {showOptions && (
          <div className="threads-list-item-col-icon">
            <ThreadsListItemIcon thread={thread} />
          </div>
        )}
        <div className="threads-list-item-col-title">
          <a href={thread.url.index} className="threads-list-item-title">
            {thread.title}
          </a>
          <a
            href={isNew ? thread.url.new_post : thread.url.index}
            className={
              "threads-list-item-title-sm" +
              (isNew ? " threads-list-item-title-new" : "")
            }
          >
            {thread.title}
          </a>
        </div>
        {showOptions && thread.moderation.length > 0 && (
          <div className="threads-list-item-col-checkbox-sm">
            <ThreadsListItemCheckbox
              checked={isSelected}
              disabled={isBusy}
              thread={thread}
            />
          </div>
        )}
      </div>
      <div className="threads-list-item-bottom-row">
        {hasFlags && (
          <div className="threads-list-item-col-flags">
            <ThreadFlags thread={thread} />
          </div>
        )}
        {!!category && (
          <div className="threads-list-item-col-category">
            <ThreadsListItemCategory parent={parent} category={category} />
          </div>
        )}
        <div className="threads-list-item-col-spacer-xs" />
        <div className="threads-list-item-col-replies">
          <ThreadReplies thread={thread} />
        </div>
        <div className="threads-list-item-col-last-poster">
          <ThreadsListItemLastPoster thread={thread} />
        </div>
        <div className="threads-list-item-col-last-activity">
          <ThreadsListItemActivity thread={thread} />
        </div>
        {showOptions && showSubscription && (
          <div className="threads-list-item-col-subscription">
            <ThreadsListItemSubscription disabled={isBusy} thread={thread} />
          </div>
        )}
        {showOptions && thread.moderation.length > 0 && (
          <div className="threads-list-item-col-checkbox">
            <ThreadsListItemCheckbox
              checked={isSelected}
              disabled={isBusy}
              thread={thread}
            />
          </div>
        )}
      </div>
    </li>
  )
}

export default ThreadsListItem
