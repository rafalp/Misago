import React from "react"
import * as actions from "./controls/actions"
import LikesModal from "misago/components/post-likes"
import modal from "misago/services/modal"
import posting from "misago/services/posting"

export default function (props) {
  if (!isVisible(props.post)) return null

  return (
    <div className="post-footer">
      <MarkAsBestAnswer {...props} />
      <MarkAsBestAnswerCompact {...props} />
      <Like {...props} />
      <Likes
        lastLikes={props.post.last_likes}
        likes={props.post.likes}
        {...props}
      />
      <LikesCompact likes={props.post.likes} {...props} />
      <Reply {...props} />
      <Quote {...props} />
      <Edit {...props} />
    </div>
  )
}

export function isVisible(post) {
  return (
    (!post.is_hidden || post.acl.can_see_hidden) &&
    (post.acl.can_reply ||
      post.acl.can_edit ||
      (post.acl.can_see_likes && (post.last_likes || []).length) ||
      post.acl.can_like)
  )
}

export class MarkAsBestAnswer extends React.Component {
  onClick = () => {
    actions.markAsBestAnswer(this.props)
  }

  render() {
    const { post, thread } = this.props

    if (!thread.acl.can_mark_best_answer) return null
    if (!post.acl.can_mark_as_best_answer) return null
    if (thread.best_answer && !thread.acl.can_change_best_answer) return null

    return (
      <button
        className="hidden-xs btn btn-default btn-sm pull-left"
        disabled={this.props.post.isBusy || post.id === thread.best_answer}
        onClick={this.onClick}
        type="button"
      >
        <span className="material-icon">check_box</span>
        {pgettext("post footer btn", "Best answer")}
      </button>
    )
  }
}

export class MarkAsBestAnswerCompact extends React.Component {
  onClick = () => {
    actions.markAsBestAnswer(this.props)
  }

  render() {
    const { post, thread } = this.props

    if (!thread.acl.can_mark_best_answer) return null
    if (!post.acl.can_mark_as_best_answer) return null
    if (thread.best_answer && !thread.acl.can_change_best_answer) return null

    return (
      <button
        className="visible-xs-inline-block btn btn-default btn-sm pull-left"
        disabled={this.props.post.isBusy || post.id === thread.best_answer}
        onClick={this.onClick}
        type="button"
      >
        <span className="material-icon">check_box</span>
      </button>
    )
  }
}

export class Like extends React.Component {
  onClick = () => {
    if (this.props.post.is_liked) {
      actions.unlike(this.props)
    } else {
      actions.like(this.props)
    }
  }

  render() {
    if (!this.props.post.acl.can_like) return null

    let className = "btn btn-default btn-sm pull-left"
    if (this.props.post.is_liked) {
      className = "btn btn-success btn-sm pull-left"
    }

    return (
      <button
        className={className}
        disabled={this.props.post.isBusy}
        onClick={this.onClick}
        type="button"
      >
        {this.props.post.is_liked
          ? pgettext("post footer btn", "Liked")
          : pgettext("post footer btn", "Like")}
      </button>
    )
  }
}

export class Likes extends React.Component {
  onClick = () => {
    modal.show(<LikesModal post={this.props.post} />)
  }

  render() {
    const hasLikes = (this.props.post.last_likes || []).length > 0
    if (!this.props.post.acl.can_see_likes || !hasLikes) return null

    if (this.props.post.acl.can_see_likes === 2) {
      return (
        <button
          className="btn btn-link btn-sm pull-left hidden-xs"
          onClick={this.onClick}
          type="button"
        >
          {getLikesMessage(this.props.likes, this.props.lastLikes)}
        </button>
      )
    }

    return (
      <p className="pull-left hidden-xs">
        {getLikesMessage(this.props.likes, this.props.lastLikes)}
      </p>
    )
  }
}

export class LikesCompact extends Likes {
  render() {
    const hasLikes = (this.props.post.last_likes || []).length > 0
    if (!this.props.post.acl.can_see_likes || !hasLikes) return null

    if (this.props.post.acl.can_see_likes === 2) {
      return (
        <button
          className="btn btn-link btn-sm likes-compact pull-left visible-xs-block"
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">favorite</span>
          {this.props.likes}
        </button>
      )
    }

    return (
      <p className="likes-compact pull-left visible-xs-block">
        <span className="material-icon">favorite</span>
        {this.props.likes}
      </p>
    )
  }
}

export function getLikesMessage(likes, users) {
  const usernames = users.slice(0, 3).map((u) => u.username)

  if (usernames.length == 1) {
    return interpolate(
      pgettext("post likes", "%(user)s likes this."),
      {
        user: usernames[0],
      },
      true
    )
  }

  const hiddenLikes = likes - usernames.length

  const otherUsers = usernames.slice(0, -1).join(", ")
  const lastUser = usernames.slice(-1)[0]

  const usernamesList = interpolate(
    pgettext("post likes", "%(users)s and %(last_user)s"),
    {
      users: otherUsers,
      last_user: lastUser,
    },
    true
  )

  if (hiddenLikes === 0) {
    return interpolate(
      pgettext("post likes", "%(users)s like this."),
      {
        users: usernamesList,
      },
      true
    )
  }

  const message = npgettext(
    "post likes",
    "%(users)s and %(likes)s other user like this.",
    "%(users)s and %(likes)s other users like this.",
    hiddenLikes
  )

  return interpolate(
    message,
    {
      users: usernames.join(", "),
      likes: hiddenLikes,
    },
    true
  )
}

export class Reply extends React.Component {
  onClick = () => {
    posting.open({
      mode: "REPLY",

      thread: this.props.thread,
      config: this.props.thread.api.editor,
      submit: this.props.thread.api.posts.index,
    })
  }

  render() {
    if (this.props.post.acl.can_reply) {
      return (
        <button
          className="btn btn-default btn-sm pull-right"
          type="button"
          onClick={this.onClick}
        >
          {pgettext("post footer btn", "Reply")}
        </button>
      )
    } else {
      return null
    }
  }
}

export class Quote extends React.Component {
  onClick = () => {
    posting.open({
      mode: "QUOTE",

      thread: this.props.thread,
      config: this.props.thread.api.editor,
      submit: this.props.thread.api.posts.index,

      context: {
        reply: this.props.post.id,
      },
    })
  }

  render() {
    if (this.props.post.acl.can_reply) {
      return (
        <button
          className="btn btn-default btn-sm pull-right"
          type="button"
          onClick={this.onClick}
        >
          {pgettext("post footer btn", "Quote")}
        </button>
      )
    } else {
      return null
    }
  }
}

export class Edit extends React.Component {
  onClick = () => {
    posting.open({
      mode: "EDIT",

      thread: this.props.thread,
      post: this.props.post,
      config: this.props.post.api.editor,
      submit: this.props.post.api.index,
    })
  }

  render() {
    if (this.props.post.acl.can_edit) {
      return (
        <button
          className="hidden-xs btn btn-default btn-sm pull-right"
          type="button"
          onClick={this.onClick}
        >
          {pgettext("post footer btn", "Edit")}
        </button>
      )
    } else {
      return null
    }
  }
}
