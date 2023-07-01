import React from "react"
import UserStatus, { StatusLabel } from "misago/components/user-status"

export default function ({ showStatus, user }) {
  return (
    <ul className="list-unstyled">
      <Status showStatus={showStatus} user={user} />
      <JoinDate user={user} />
      <li className="user-stat-divider" />
      <Posts user={user} />
      <Threads user={user} />
      <Followers user={user} />
    </ul>
  )
}

export function Status({ showStatus, user }) {
  if (!showStatus) return null

  return (
    <li className="user-stat-status">
      <UserStatus status={user.status}>
        <StatusLabel status={user.status} user={user} />
      </UserStatus>
    </li>
  )
}

export function JoinDate({ user }) {
  const { joined_on } = user

  let title = interpolate(
    pgettext("users list item", "Joined on %(joined_on)s"),
    {
      joined_on: joined_on.format("LL, LT"),
    },
    true
  )

  let message = interpolate(
    pgettext("users list item", "Joined %(joined_on)s"),
    {
      joined_on: joined_on.fromNow(),
    },
    true
  )

  return (
    <li className="user-stat-join-date">
      <abbr title={title}>{message}</abbr>
    </li>
  )
}

export function Posts({ user }) {
  const className = getStatClassName("user-stat-posts", user.posts)
  const message = npgettext(
    "users list item",
    "%(posts)s post",
    "%(posts)s posts",
    user.posts
  )

  return (
    <li className={className}>
      {interpolate(
        message,
        {
          posts: user.posts,
        },
        true
      )}
    </li>
  )
}

export function Threads({ user }) {
  const className = getStatClassName("user-stat-threads", user.threads)
  const message = npgettext(
    "users list item",
    "%(threads)s thread",
    "%(threads)s threads",
    user.threads
  )

  return (
    <li className={className}>
      {interpolate(
        message,
        {
          threads: user.threads,
        },
        true
      )}
    </li>
  )
}

export function Followers({ user }) {
  const className = getStatClassName("user-stat-followers", user.followers)
  const message = npgettext(
    "users list item",
    "%(followers)s follower",
    "%(followers)s followers",
    user.followers
  )

  return (
    <li className={className}>
      {interpolate(
        message,
        {
          followers: user.followers,
        },
        true
      )}
    </li>
  )
}

export function getStatClassName(className, stat) {
  if (stat === 0) {
    return className + " user-stat-empty"
  }
  return className
}
