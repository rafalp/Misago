import React from "react"

const ThreadShortcutsButton = ({ user, thread }) => (
  <div className="dropdown">
    <button
      className="btn btn-default btn-outline btn-icon"
      title={gettext("Shortcuts")}
      aria-expanded="true"
      aria-haspopup="true"
      data-toggle="dropdown"
      type="button"
    >
      <span className="material-icon">bookmark</span>
    </button>
    <ul className="dropdown-menu">
      {user.is_authenticated && thread.is_new && (
        <li>
          <a className="btn btn-link" href={thread.url.new_post}>
            <span className="material-icon">comment</span>
            {gettext("Go to new post")}
          </a>
        </li>
      )}
      {thread.best_answer && (
        <li>
          <a className="btn btn-link" href={thread.url.best_answer}>
            <span className="material-icon">check_circle</span>
            {gettext("Go to best answer")}
          </a>
        </li>
      )}
      {thread.has_unapproved_posts && thread.acl.can_approve && (
        <li>
          <a className="btn btn-link" href={thread.url.unapproved_post}>
            <span className="material-icon">visibility</span>
            {gettext("Go to unapproved post")}
          </a>
        </li>
      )}
      <li>
        <a className="btn btn-link" href={thread.url.last_post}>
          <span className="material-icon">reply</span>
          {gettext("Go to last post")}
        </a>
      </li>
    </ul>
  </div>
)

export default ThreadShortcutsButton
