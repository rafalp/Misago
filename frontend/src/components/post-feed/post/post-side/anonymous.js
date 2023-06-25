import React from "react"
import Avatar from "misago/components/avatar"
import GoToButton from "./button"

export default function ({ post }) {
  return (
    <div className="post-side post-side-anonymous">
      <GoToButton post={post} />
      <div className="media">
        <div className="media-left">
          <span>
            <Avatar className="poster-avatar" size={50} />
          </span>
        </div>
        <div className="media-body">
          <div className="media-heading">
            <span className="item-title">{post.poster_name}</span>
          </div>
          <span className="user-title user-title-anonymous">
            {pgettext("post removed poster username", "Removed user")}
          </span>
        </div>
      </div>
    </div>
  )
}
