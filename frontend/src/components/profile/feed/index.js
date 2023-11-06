import React from "react"
import Route from "./route"

export function Threads(props) {
  let emptyMessage = null
  if (props.user.id === props.profile.id) {
    emptyMessage = pgettext(
      "profile threads",
      "You haven't started any threads."
    )
  } else {
    emptyMessage = interpolate(
      pgettext("profile threads", "%(username)s hasn't started any threads"),
      {
        username: props.profile.username,
      },
      true
    )
  }

  let header = null
  if (!props.posts.isLoaded) {
    header = pgettext("profile threads", "Loading...")
  } else if (props.profile.id === props.user.id) {
    const message = npgettext(
      "profile threads",
      "You have started %(threads)s thread.",
      "You have started %(threads)s threads.",
      props.profile.threads
    )

    header = interpolate(
      message,
      {
        threads: props.profile.threads,
      },
      true
    )
  } else {
    const message = npgettext(
      "profile threads",
      "%(username)s has started %(threads)s thread.",
      "%(username)s has started %(threads)s threads.",
      props.profile.threads
    )

    header = interpolate(
      message,
      {
        username: props.profile.username,
        threads: props.profile.threads,
      },
      true
    )
  }

  return (
    <Route
      api={props.profile.api.threads}
      emptyMessage={emptyMessage}
      header={header}
      title={pgettext("profile threads title", "Threads")}
      {...props}
    />
  )
}

export function Posts(props) {
  let emptyMessage = null
  if (props.user.id === props.profile.id) {
    emptyMessage = pgettext("profile posts", "You have posted no messages.")
  } else {
    emptyMessage = interpolate(
      pgettext("profile posts", "%(username)s posted no messages."),
      {
        username: props.profile.username,
      },
      true
    )
  }

  let header = null
  if (!props.posts.isLoaded) {
    header = pgettext("profile posts", "Loading...")
  } else if (props.profile.id === props.user.id) {
    const message = npgettext(
      "profile posts",
      "You have posted %(posts)s message.",
      "You have posted %(posts)s messages.",
      props.profile.posts
    )

    header = interpolate(
      message,
      {
        posts: props.profile.posts,
      },
      true
    )
  } else {
    const message = npgettext(
      "profile posts",
      "%(username)s has posted %(posts)s message.",
      "%(username)s has posted %(posts)s messages.",
      props.profile.posts
    )

    header = interpolate(
      message,
      {
        username: props.profile.username,
        posts: props.profile.posts,
      },
      true
    )
  }

  return (
    <Route
      api={props.profile.api.posts}
      emptyMessage={emptyMessage}
      header={header}
      title={pgettext("profile posts title", "Posts")}
      {...props}
    />
  )
}
