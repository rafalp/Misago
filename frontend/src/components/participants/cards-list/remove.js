import React from "react"
import { remove, leave } from "./actions"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.isUser = props.participant.id === props.user.id
  }

  onClick = () => {
    let confirmed = false
    if (this.isUser) {
      confirmed = window.confirm(
        pgettext(
          "private thread leave",
          "Are you sure you want to leave this thread?"
        )
      )
    } else {
      const message = pgettext(
        "private thread leave",
        "Are you sure you want to remove %(user)s from this thread?"
      )
      confirmed = window.confirm(
        interpolate(
          message,
          {
            user: this.props.participant.username,
          },
          true
        )
      )
    }

    if (!confirmed) return

    if (this.isUser) {
      leave(this.props.thread, this.props.participant)
    } else {
      remove(this.props.thread, this.props.participant)
    }
  }

  render() {
    const isModerator = this.props.user.acl.can_moderate_private_threads

    if (!(this.props.userIsOwner || this.isUser || isModerator)) return null

    return (
      <li>
        <button className="btn btn-link" onClick={this.onClick} type="button">
          {this.isUser
            ? pgettext("private thread leave btn", "Leave thread")
            : pgettext("private thread leave btn", "Remove")}
        </button>
      </li>
    )
  }
}
