import React from "react"

const ThreadReplies = ({ thread }) => (
  <span
    className="threads-replies"
    title={interpolate(
      npgettext(
        "thread replies stat",
        "%(replies)s reply",
        "%(replies)s replies",
        thread.replies
      ),
      { replies: thread.replies },
      true
    )}
  >
    <span className="material-icon">chat_bubble_outline</span>
    {thread.replies > 980
      ? Math.round(thread.replies / 1000) + "K"
      : thread.replies}
  </span>
)

export default ThreadReplies
