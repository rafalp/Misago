import React from "react"

const ThreadPostsLeft = ({ posts }) => {
  if (posts.more) {
    return (
      <p>
        {interpolate(
          ngettext(
            "There is %(more)s more post in this thread.",
            "There are %(more)s more posts in this thread.",
            posts.more
          ),
          { more: posts.more },
          true
        )}
      </p>
    )
  }

  return <p>{gettext("There are no more posts in this thread.")}</p>
}

export default ThreadPostsLeft
