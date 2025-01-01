import React from "react"
import Controls from "./controls"
import Select from "./select"
import {
  StatusIcon,
  getStatusClassName,
  getStatusDescription,
} from "misago/components/user-status"
import PostChangelog from "misago/components/post-changelog"
import Timestamp from "misago/components/Timestamp"
import modal from "misago/services/modal"

export default function (props) {
  return (
    <div className="post-heading">
      <UnreadLabel {...props} />
      <UnreadCompact {...props} />
      <PostedOn {...props} />
      <PostedOnCompact {...props} />
      <PostEdits {...props} />
      <PostEditsCompacts {...props} />
      <ProtectedLabel {...props} />
      <Select {...props} />
      <Controls {...props} />
    </div>
  )
}

export function UnreadLabel(props) {
  if (props.post.is_read) return null

  return (
    <span className="label label-unread hidden-xs">
      {pgettext("post unread label", "New post")}
    </span>
  )
}

export function UnreadCompact(props) {
  if (props.post.is_read) return null

  return (
    <span className="label label-unread visible-xs-inline-block">
      {pgettext("post unread label", "New")}
    </span>
  )
}

export function PostedOn(props) {
  return (
    <a href={props.post.url.index} className="btn btn-link posted-on hidden-xs">
      <Timestamp datetime={props.post.posted_on.toISOString()} />
    </a>
  )
}

export function PostedOnCompact(props) {
  return (
    <a
      href={props.post.url.index}
      className="btn btn-link posted-on visible-xs-inline-block"
    >
      {props.post.posted_on.fromNow()}
    </a>
  )
}

export class PostEdits extends React.Component {
  onClick = () => {
    modal.show(<PostChangelog post={this.props.post} />)
  }

  render() {
    const isHidden =
      this.props.post.is_hidden && !this.props.post.acl.can_see_hidden
    const isUnedited = this.props.post.edits === 0
    if (isHidden || isUnedited) return null

    const tooltip = npgettext(
      "post edits stat",
      "This post was edited %(edits)s time.",
      "This post was edited %(edits)s times.",
      this.props.post.edits
    )

    const title = interpolate(
      tooltip,
      {
        edits: this.props.post.edits,
      },
      true
    )

    const label = npgettext(
      "post edits stat",
      "edited %(edits)s time",
      "edited %(edits)s times",
      this.props.post.edits
    )

    return (
      <button
        className="btn btn-link btn-see-edits hidden-xs"
        onClick={this.onClick}
        title={title}
        type="button"
      >
        {interpolate(
          label,
          {
            edits: this.props.post.edits,
          },
          true
        )}
      </button>
    )
  }
}

export class PostEditsCompacts extends PostEdits {
  render() {
    const isHidden =
      this.props.post.is_hidden && !this.props.post.acl.can_see_hidden
    const isUnedited = this.props.post.edits === 0
    if (isHidden || isUnedited) return null

    const label = npgettext(
      "post edits stat",
      "%(edits)s edit",
      "%(edits)s edits",
      this.props.post.edits
    )

    return (
      <button
        className="btn btn-link btn-see-edits visible-xs-inline-block"
        onClick={this.onClick}
        type="button"
      >
        {interpolate(
          label,
          {
            edits: this.props.post.edits,
          },
          true
        )}
      </button>
    )
  }
}

export function ProtectedLabel(props) {
  const postAuthor = props.post.poster && props.post.poster.id === props.user.id
  const hasAcl = props.post.acl.can_protect
  const isVisible =
    props.user.id && props.post.is_protected && (postAuthor || hasAcl)

  if (!isVisible) {
    return null
  }

  return (
    <span
      className="label label-protected hidden-xs"
      title={pgettext(
        "post protected label",
        "This post is protected and may not be edited."
      )}
    >
      <span className="material-icon">lock_outline</span>
      {pgettext("post protected label", "protected")}
    </span>
  )
}
