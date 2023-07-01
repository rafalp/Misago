import React from "react"

export default function ({ category }) {
  return (
    <div className="col-md-2 hidden-xs hidden-sm">
      <ul className="list-unstyled category-stats">
        <Threads threads={category.threads} />
        <Posts posts={category.posts} />
      </ul>
    </div>
  )
}

export function Threads({ threads }) {
  const message = npgettext(
    "category stats",
    "%(threads)s thread",
    "%(threads)s threads",
    threads
  )

  return (
    <li className="category-stat-threads">
      {interpolate(
        message,
        {
          threads: threads,
        },
        true
      )}
    </li>
  )
}

export function Posts({ posts }) {
  const message = npgettext(
    "category stats",
    "%(posts)s post",
    "%(posts)s posts",
    posts
  )

  return (
    <li className="category-stat-posts">
      {interpolate(
        message,
        {
          posts: posts,
        },
        true
      )}
    </li>
  )
}
