import React from "react"
import Avatar from "misago/components/avatar"
import Controls from "misago/components/posts-list/post/controls"
import Select from "misago/components/posts-list/post/select"
import UserStatus, { StatusIcon } from "misago/components/user-status"
import UserPostcount from "./user-postcount"
import UserStatusLabel from "./user-status"
import UserTitle from "./user-title"

export default function ({ post, thread }) {
  const { poster } = post

  return (
    <div className="post-side post-side-registered">
      <Select post={post} thread={thread} />
      <Controls post={post} thread={thread} />
      <div className="media">
        <div className="media-left">
          <a href={poster.url}>
            <Avatar className="poster-avatar" size={100} user={poster} />
          </a>
        </div>
        <div className="media-body">
          <div className="media-heading">
            <a className="item-title" href={poster.url}>
              {poster.username}
            </a>
            <UserStatus status={poster.status}>
              <StatusIcon status={poster.status} />
            </UserStatus>
          </div>

          <UserTitle rank={poster.rank} title={poster.title} />

          <UserStatusLabel poster={poster} />
          <UserPostcount poster={poster} />
        </div>
      </div>
    </div>
  )
}
