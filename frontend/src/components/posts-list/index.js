import React from "react"
import Event from "./event"
import Post from "./post"
import PostPreview from "./post/preview"

export default function (props) {
  if (!props.posts.isLoaded) {
    return (
      <ul className="posts-list ui-preview">
        <PostPreview />
      </ul>
    )
  }

  return (
    <ul className="posts-list ui-ready">
      {props.posts.results.map((post) => {
        return <ListItem key={post.id} post={post} {...props} />
      })}
    </ul>
  )
}

export function ListItem(props) {
  if (props.post.is_event) {
    return <Event {...props} />
  }

  return <Post {...props} />
}
