import React from "react"
import { Link } from "react-router"

const ThreadShortcutsButton = ({ user, thread, posts }) => (
  <div className="dropdown">
    <button
      className="btn btn-default btn-outline btn-icon"
      title={pgettext("thread shortcuts btn", "Shortcuts")}
      aria-expanded="true"
      aria-haspopup="true"
      data-toggle="dropdown"
      type="button"
    >
      <span className="material-icon">bookmark</span>
    </button>
    <ul className="dropdown-menu">
      {!!posts.first && (
        <li>
          <Link className="btn btn-link" href={thread.url.index}>
            <span className="material-icon">place</span>
            {pgettext("thread shortcut btn", "Go to first post")}
          </Link>
        </li>
      )}
      {user.is_authenticated && thread.is_new && (
        <li>
          <a className="btn btn-link" href={thread.url.new_post}>
            <span className="material-icon">comment</span>
            {pgettext("thread shortcut btn", "Go to new post")}
          </a>
        </li>
      )}
      {thread.best_answer && (
        <li>
          <a className="btn btn-link" href={thread.url.best_answer}>
            <span className="material-icon">check_circle</span>
            {pgettext("thread shortcut btn", "Go to best answer")}
          </a>
        </li>
      )}
      {thread.has_unapproved_posts && thread.acl.can_approve && (
        <li>
          <a className="btn btn-link" href={thread.url.unapproved_post}>
            <span className="material-icon">visibility</span>
            {pgettext("thread shortcut btn", "Go to unapproved post")}
          </a>
        </li>
      )}
      <li>
        <a className="btn btn-link" href={thread.url.last_post}>
          <span className="material-icon">reply</span>
          {pgettext("thread shortcut btn", "Go to last post")}
        </a>
      </li>
    </ul>
  </div>
)

export default ThreadShortcutsButton
