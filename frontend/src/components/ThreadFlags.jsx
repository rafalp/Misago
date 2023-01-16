import React from "react"

const ThreadFlags = ({ thread }) => (
  <ul className="thread-flags">
    {thread.weight == 2 && (
      <li
        className="thread-flag-pinned-globally"
        title={gettext("Pinned globally")}
      >
        <span className="material-icon">bookmark</span>
      </li>
    )}
    {thread.weight == 1 && (
      <li
        className="thread-flag-pinned-locally"
        title={gettext("Pinned in category")}
      >
        <span className="material-icon">bookmark_outline</span>
      </li>
    )}
    {thread.best_answer && (
      <li className="thread-flag-answered" title={gettext("Answered")}>
        <span className="material-icon">check_circle</span>
      </li>
    )}
    {thread.has_poll && (
      <li className="thread-flag-poll" title={gettext("Poll")}>
        <span className="material-icon">poll</span>
      </li>
    )}
    {(thread.is_unapproved || thread.has_unapproved_posts) && (
      <li
        className="thread-flag-unapproved"
        title={
          thread.is_unapproved
            ? gettext("Awaiting approval")
            : gettext("Has unapproved posts")
        }
      >
        <span className="material-icon">visibility</span>
      </li>
    )}
    {thread.is_closed && (
      <li className="thread-flag-closed" title={gettext("Closed")}>
        <span className="material-icon">lock</span>
      </li>
    )}
    {thread.is_hidden && (
      <li className="thread-flag-hidden" title={gettext("Hidden")}>
        <span className="material-icon">visibility_off</span>
      </li>
    )}
  </ul>
)

export default ThreadFlags
