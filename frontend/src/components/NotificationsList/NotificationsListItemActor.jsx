import React from "react"
import Avatar from "../avatar"

export default function NotificationsListItemActor({ notification }) {
  if (!!notification.actor) {
    return (
      <a
        href={notification.actor.url}
        className="notifications-list-item-actor"
        title={notification.actor.username}
      >
        <Avatar size={30} user={notification.actor} />
      </a>
    )
  }

  return (
    <span
      className="threads-list-item-last-poster"
      title={notification.actor_name || null}
    >
      <Avatar size={30} />
    </span>
  )
}
