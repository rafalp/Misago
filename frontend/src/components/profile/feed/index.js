import React from "react"
import Route from "./route"

export function Threads(props) {
  let emptyMessage = null
  if (props.user.id === props.profile.id) {
    emptyMessage = gettext("You have no started threads.")
  } else {
    emptyMessage = interpolate(
      gettext("%(username)s started no threads."),
      {
        username: props.profile.username
      },
      true
    )
  }

  let header = null
  if (!props.posts.isLoaded) {
    header = gettext("Loading...")
  } else if (props.profile.id === props.user.id) {
    const message = ngettext(
      "You have started %(threads)s thread.",
      "You have started %(threads)s threads.",
      props.profile.threads
    )

    header = interpolate(
      message,
      {
        threads: props.profile.threads
      },
      true
    )
  } else {
    const message = ngettext(
      "%(username)s has started %(threads)s thread.",
      "%(username)s has started %(threads)s threads.",
      props.profile.threads
    )

    header = interpolate(
      message,
      {
        username: props.profile.username,
        threads: props.profile.threads
      },
      true
    )
  }

  return (
    <Route
      api={props.profile.api.threads}
      emptyMessage={emptyMessage}
      header={header}
      title={gettext("Threads")}
      {...props}
    />
  )
}

export function Posts(props) {
  let emptyMessage = null
  if (props.user.id === props.profile.id) {
    emptyMessage = gettext("You have posted no messages.")
  } else {
    emptyMessage = interpolate(
      gettext("%(username)s posted no messages."),
      {
        username: props.profile.username
      },
      true
    )
  }

  let header = null
  if (!props.posts.isLoaded) {
    header = gettext("Loading...")
  } else if (props.profile.id === props.user.id) {
    const message = ngettext(
      "You have posted %(posts)s message.",
      "You have posted %(posts)s messages.",
      props.profile.posts
    )

    header = interpolate(
      message,
      {
        posts: props.profile.posts
      },
      true
    )
  } else {
    const message = ngettext(
      "%(username)s has posted %(posts)s message.",
      "%(username)s has posted %(posts)s messages.",
      props.profile.posts
    )

    header = interpolate(
      message,
      {
        username: props.profile.username,
        posts: props.profile.posts
      },
      true
    )
  }

  return (
    <Route
      api={props.profile.api.posts}
      emptyMessage={emptyMessage}
      header={header}
      title={gettext("Posts")}
      {...props}
    />
  )
}
