import React from "react"
import Post from "./post"
import Preview from "./preview"

export default function ({ isReady, posts, poster }) {
  if (!isReady) {
    return <Preview />
  }

  return (
    <ul className="posts-list post-feed ui-ready">
      {posts.map((post) => {
        return <Post key={post.id} post={post} poster={poster} />
      })}
    </ul>
  )
}
