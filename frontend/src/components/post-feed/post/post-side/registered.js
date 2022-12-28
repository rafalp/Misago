import React from "react"
import Avatar from "misago/components/avatar"
import GoToButton from "./button"
import UserTitle from "./user-title"

export default function ({ post, poster }) {
  return (
    <div className="post-side post-side-registered">
      <GoToButton post={post} />
      <div className="media">
        <div className="media-left">
          <a href={poster.url}>
            <Avatar className="poster-avatar" size={50} user={poster} />
          </a>
        </div>
        <div className="media-body">
          <div className="media-heading">
            <a className="item-title" href={poster.url}>
              {poster.username}
            </a>
          </div>
          <UserTitle title={poster.title} rank={poster.rank} />
        </div>
      </div>
    </div>
  )
}
