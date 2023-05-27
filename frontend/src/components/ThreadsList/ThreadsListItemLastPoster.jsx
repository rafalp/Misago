import React from "react"
import Avatar from "../avatar"

const ThreadsListItemLastPoster = ({ thread }) =>
  !!thread.last_poster ? (
    <a
      href={thread.url.last_poster}
      className="threads-list-item-last-poster"
      title={interpolate(
        pgettext("threads list", "%(poster)s - latest poster"),
        { poster: thread.last_poster.username },
        true
      )}
    >
      <Avatar size={30} user={thread.last_poster} />
    </a>
  ) : (
    <span
      className="threads-list-item-last-poster"
      title={interpolate(
        pgettext("threads list", "%(poster)s - latest poster"),
        { poster: thread.last_poster_name },
        true
      )}
    >
      <Avatar size={30} />
    </span>
  )

export default ThreadsListItemLastPoster
