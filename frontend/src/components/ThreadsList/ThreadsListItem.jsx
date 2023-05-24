import classnames from "classnames"
import React from "react"
import ThreadFlags from "../ThreadFlags"
import ThreadReplies from "../ThreadReplies"
import ThreadsListItemActivity from "./ThreadsListItemActivity"
import ThreadsListItemCategory from "./ThreadsListItemCategory"
import ThreadsListItemCheckbox from "./ThreadsListItemCheckbox"
import ThreadsListItemLastPoster from "./ThreadsListItemLastPoster"
import ThreadsListItemNotifications from "./ThreadsListItemNotifications"
import ThreadsListItemReadStatus from "./ThreadsListItemReadStatus"
import ThreadsListItemStarter from "./ThreadsListItemStarter"
import ThreadsListItemTitle from "./ThreadsListItemTitle"

const ThreadsListItem = ({
  activeCategory,
  categories,
  showOptions,
  showNotifications,
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

  const isNew = showOptions ? thread.is_new : false

  return (
    <li
      className={classnames("list-group-item threads-list-item", {
        "threads-list-item-is-busy": isBusy,
      })}
    >
      <div className="threads-list-item-col-starter">
        <ThreadsListItemStarter thread={thread} />
      </div>
      {showOptions && (
        <div className="threads-list-item-col-read-status">
          <ThreadsListItemReadStatus thread={thread} />
        </div>
      )}
      <div className="threads-list-item-right-col">
        <div className="threads-list-item-top-row">
          <ThreadsListItemTitle thread={thread} isNew={isNew} />
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
          <div className="threads-list-item-bottom-left">
            <div className="threads-list-item-col-starter-sm">
              <ThreadsListItemStarter thread={thread} />
            </div>
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
          </div>
          <div className="threads-list-item-bottom-right">
            <div
              className={classnames("threads-list-item-col-replies", {
                "threads-list-item-col-replies-zero": thread.replies === 0,
              })}
            >
              <ThreadReplies thread={thread} />
            </div>
            <div className="threads-list-item-col-last-poster">
              <ThreadsListItemLastPoster thread={thread} />
            </div>
            <div className="threads-list-item-col-last-activity">
              <ThreadsListItemActivity thread={thread} />
            </div>
            <div className="threads-list-item-col-last-poster-sm">
              <ThreadsListItemLastPoster thread={thread} />
            </div>
            {showOptions && showNotifications && (
              <div className="threads-list-item-col-notifications">
                <ThreadsListItemNotifications
                  disabled={isBusy}
                  thread={thread}
                />
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
        </div>
      </div>
    </li>
  )
}

export default ThreadsListItem
