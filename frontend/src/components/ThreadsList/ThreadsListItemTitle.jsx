import classnames from "classnames"
import React from "react"

const ThreadsListItemTitle = ({ thread, isNew }) => (
  <div className="threads-list-item-col-title">
    <a
      href={isNew ? thread.url.new_post : thread.url.index}
      className={classnames("threads-list-item-title", {
        "threads-list-item-title-new": isNew,
      })}
    >
      {thread.title}
    </a>
    {getPagesRange(thread.pages).map((page) => (
      <a
        key={page}
        href={thread.url.index + page + "/"}
        className="threads-list-item-goto-page"
        title={pgettext("threads list", "Go to page: %(page)s").replace(
          "%(page)s",
          page
        )}
      >
        {page}
      </a>
    ))}
  </div>
)

function getPagesRange(pages) {
  const range = []
  if (pages > 3) {
    range.push(pages - 2)
  }
  if (pages > 2) {
    range.push(pages - 1)
  }
  if (pages > 1) {
    range.push(pages)
  }
  return range
}

export default ThreadsListItemTitle
