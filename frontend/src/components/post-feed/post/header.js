import React from "react"

export default function ({ post }) {
  const { category, thread } = post

  const tooltip = interpolate(
    pgettext("posts feed item header", "posted %(posted_on)s"),
    {
      posted_on: post.posted_on.format("LL, LT"),
    },
    true
  )

  return (
    <div className="post-heading">
      <a className="btn btn-link item-title" href={thread.url}>
        {thread.title}
      </a>
      <a className="btn btn-link post-category" href={category.url.index}>
        {category.name}
      </a>
      <a
        href={post.url.index}
        className="btn btn-link posted-on"
        title={tooltip}
      >
        {post.posted_on.fromNow()}
      </a>
    </div>
  )
}
