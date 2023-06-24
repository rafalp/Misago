import React from "react"

export function FlagBestAnswer({ post, thread, user }) {
  if (!(isVisible(post) && post.id === thread.best_answer)) {
    return null
  }

  let message = null
  if (user.id && thread.best_answer_marked_by === user.id) {
    message = interpolate(
      pgettext(
        "post best answer flag",
        "Marked as best answer by you %(marked_on)s."
      ),
      {
        marked_on: thread.best_answer_marked_on.fromNow(),
      },
      true
    )
  } else {
    message = interpolate(
      pgettext(
        "post best answer flag",
        "Marked as best answer by %(marked_by)s %(marked_on)s."
      ),
      {
        marked_by: thread.best_answer_marked_by_name,
        marked_on: thread.best_answer_marked_on.fromNow(),
      },
      true
    )
  }

  return (
    <div className="post-status-message post-status-best-answer">
      <span className="material-icon">check_box</span>
      <p>{message}</p>
    </div>
  )
}

export function FlagHidden(props) {
  if (!(isVisible(props.post) && props.post.is_hidden)) {
    return null
  }

  return (
    <div className="post-status-message post-status-hidden">
      <span className="material-icon">visibility_off</span>
      <p>
        {pgettext(
          "post hidden flag",
          "This post is hidden. Only users with permission may see its contents."
        )}
      </p>
    </div>
  )
}

export function FlagUnapproved(props) {
  if (!(isVisible(props.post) && props.post.is_unapproved)) {
    return null
  }

  return (
    <div className="post-status-message post-status-unapproved">
      <span className="material-icon">remove_circle_outline</span>
      <p>
        {pgettext(
          "post unapproved flag",
          "This post is unapproved. Only users with permission to approve posts and its author may see its contents."
        )}
      </p>
    </div>
  )
}

export function FlagProtected(props) {
  if (!(isVisible(props.post) && props.post.is_protected)) {
    return null
  }

  return (
    <div className="post-status-message post-status-protected visible-xs-block">
      <span className="material-icon">lock_outline</span>
      <p>
        {pgettext(
          "post protected flag",
          "This post is protected. Only moderators may change it."
        )}
      </p>
    </div>
  )
}

export function isVisible(post) {
  return !post.is_hidden || post.acl.can_see_hidden
}
