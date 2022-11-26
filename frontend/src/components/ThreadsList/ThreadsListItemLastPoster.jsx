import React from "react"
import Avatar from "../avatar"

const ThreadsListItemLastPoster = ({ thread }) => (
  !!thread.last_poster ? (
    <a
      href={thread.url.last_poster}
      className="threads-list-item-last-poster"
      title={interpolate(
        gettext("Last post by: %(poster)s"),
        {poster: thread.last_poster.username},
        true
      )}
    >
      <Avatar size={32} user={thread.last_poster} />
    </a>
  )
  : (
    <span
      className="threads-list-item-last-poster"
      title={interpolate(
        gettext("Last post by: %(poster)s"),
        {poster: thread.last_poster_name},
        true
      )}
    >
      <Avatar size={32} />
    </span>
  )
)

export default ThreadsListItemLastPoster