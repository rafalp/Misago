import React from "react"
import { ThreadPostsModerationOptions } from "./moderation/posts"

const ThreadPostsModeration = ({ thread, user, selection, dropup }) => (
  <div className={dropup ? "dropup" : "dropdown"}>
    <button
      type="button"
      className="btn btn-default btn-outline btn-icon dropdown-toggle"
      title={pgettext("post options btn", "Posts options")}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
      disabled={selection.length === 0}
    >
      <span className="material-icon">settings</span>
    </button>
    <ThreadPostsModerationOptions
      thread={thread}
      user={user}
      selection={selection}
    />
  </div>
)

export default ThreadPostsModeration
