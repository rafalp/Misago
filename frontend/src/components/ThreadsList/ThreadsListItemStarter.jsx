import React from "react"
import Avatar from "../avatar"

const ThreadsListItemStarter = ({ thread }) =>
  !!thread.starter ? (
    <a
      href={thread.url.starter}
      className="threads-list-item-last-poster"
      title={interpolate(
        pgettext("threads list", "%(starter)s - original poster"),
        { starter: thread.starter.username },
        true
      )}
    >
      <Avatar size={32} user={thread.starter} />
    </a>
  ) : (
    <span
      className="threads-list-item-last-poster"
      title={interpolate(
        pgettext("threads list", "%(starter)s - original poster"),
        { starter: thread.starter_name },
        true
      )}
    >
      <Avatar size={32} />
    </span>
  )

export default ThreadsListItemStarter
