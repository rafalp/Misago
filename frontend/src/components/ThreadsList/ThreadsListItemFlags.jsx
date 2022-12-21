import React from "react"

const ThreadsListItemFlags = ({ thread }) => (
  <ul className="threads-list-item-flags">
    {thread.weight == 2 && (
      <li
        className="threads-list-item-flag-pinned-globally"
        title={gettext("Pinned globally")}
      >
        <span className="material-icon">bookmark</span>
      </li>
    )}
    {thread.weight == 1 && (
      <li
        className="threads-list-item-flag-pinned-locally"
        title={gettext("Pinned in category")}
      >
        <span className="material-icon">bookmark_outline</span>
      </li>
    )}
    {thread.best_answer && (
      <li
        className="threads-list-item-flag-answered"
        title={gettext("Answered")}
      >
        <span className="material-icon">check_circle</span>
      </li>
    )}
    {thread.has_poll && (
      <li
        className="threads-list-item-flag-poll"
        title={gettext("Poll")}
      >
        <span className="material-icon">poll</span>
      </li>
    )}
    {(thread.is_unapproved || thread.has_unapproved_posts) && (
      <li
        className="threads-list-item-flag-unapproved"
        title={thread.is_unapproved ? gettext("Awaiting approval") : gettext("Has unapproved posts")}
      >
        <span className="material-icon">visibility</span>
      </li>
    )}
    {thread.is_closed && (
      <li
        className="threads-list-item-flag-closed"
        title={gettext("Closed")}
      >
        <span className="material-icon">lock</span>
      </li>
    )}
    {thread.is_hidden && (
      <li
        className="threads-list-item-flag-hidden"
        title={gettext("Hidden")}
      >
        <span className="material-icon">visibility_off</span>
      </li>
    )}
  </ul>
)

export default ThreadsListItemFlags