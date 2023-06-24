import React from "react"
import hasVisibleTitle from "./has-visible-title"

export default function ({ poster }) {
  const message = npgettext(
    "poster stats",
    "%(posts)s post",
    "%(posts)s posts",
    poster.posts
  )

  let className = "user-postcount"
  if (hasVisibleTitle(poster)) {
    className += " hidden-xs hidden-sm"
  }

  return (
    <span className={className}>
      {interpolate(
        message,
        {
          posts: poster.posts,
        },
        true
      )}
    </span>
  )
}
