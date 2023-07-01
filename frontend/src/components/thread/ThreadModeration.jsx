import React from "react"
import ThreadModerationOptions from "./moderation/thread"

const ThreadModeration = ({ thread, posts, moderation }) => (
  <div className="dropdown">
    <button
      type="button"
      className="btn btn-default btn-outline btn-icon dropdown-toggle"
      title={pgettext("thread options btn", "Thread options")}
      data-toggle="dropdown"
      aria-haspopup="true"
      aria-expanded="false"
      disabled={thread.isBusy}
    >
      <span className="material-icon">settings</span>
    </button>
    <ThreadModerationOptions
      thread={thread}
      posts={posts}
      moderation={moderation}
    />
  </div>
)

export default ThreadModeration
