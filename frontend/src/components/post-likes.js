import React from "react"
import moment from "moment"
import Avatar from "misago/components/avatar"
import Message from "misago/components/modal-message"
import Loader from "misago/components/modal-loader"
import ajax from "misago/services/ajax"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isReady: false,

      error: null,
      likes: [],
    }
  }

  componentDidMount() {
    ajax.get(this.props.post.api.likes).then(
      (data) => {
        this.setState({
          isReady: true,
          likes: data.map(hydrateLike),
        })
      },
      (rejection) => {
        this.setState({
          isReady: true,
          error: rejection.detail,
        })
      }
    )
  }

  render() {
    if (this.state.error) {
      return (
        <ModalDialog className="modal-message">
          <Message message={this.state.error} />
        </ModalDialog>
      )
    } else if (this.state.isReady) {
      if (this.state.likes.length) {
        return (
          <ModalDialog className="modal-sm" likes={this.state.likes}>
            <LikesList likes={this.state.likes} />
          </ModalDialog>
        )
      }

      return (
        <ModalDialog className="modal-message">
          <Message
            message={pgettext(
              "post likes modal",
              "No users have liked this post."
            )}
          />
        </ModalDialog>
      )
    }

    return (
      <ModalDialog className="modal-sm">
        <Loader />
      </ModalDialog>
    )
  }
}

export function hydrateLike(data) {
  return Object.assign({}, data, {
    liked_on: moment(data.liked_on),
  })
}

export function ModalDialog({ className, children, likes }) {
  let title = pgettext("post likes modal title", "Post Likes")
  if (likes) {
    const likesCount = likes.length
    const message = npgettext(
      "post likes modal",
      "%(likes)s like",
      "%(likes)s likes",
      likesCount
    )

    title = interpolate(message, { likes: likesCount }, true)
  }

  return (
    <div className={"modal-dialog " + (className || "")} role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={pgettext("modal", "Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">{title}</h4>
        </div>
        {children}
      </div>
    </div>
  )
}

export function LikesList(props) {
  return (
    <div className="modal-body modal-post-likers">
      <ul className="media-list">
        {props.likes.map((like) => {
          return <LikeDetails key={like.id} {...like} />
        })}
      </ul>
    </div>
  )
}

export function LikeDetails(props) {
  if (props.url) {
    const user = {
      id: props.liker_id,
      avatars: props.avatars,
    }

    return (
      <li className="media">
        <div className="media-left">
          <a className="user-avatar" href={props.url}>
            <Avatar size="50" user={user} />
          </a>
        </div>
        <div className="media-body">
          <a className="item-title" href={props.url}>
            {props.username}
          </a>{" "}
          <LikeDate likedOn={props.liked_on} />
        </div>
      </li>
    )
  }

  return (
    <li className="media">
      <div className="media-left">
        <span className="user-avatar">
          <Avatar size="50" />
        </span>
      </div>
      <div className="media-body">
        <strong>{props.username}</strong> <LikeDate likedOn={props.liked_on} />
      </div>
    </li>
  )
}

export function LikeDate(props) {
  return (
    <span className="text-muted" title={props.likedOn.format("LLL")}>
      {props.likedOn.fromNow()}
    </span>
  )
}
