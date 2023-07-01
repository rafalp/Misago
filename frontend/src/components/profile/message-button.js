import React from "react"
import posting from "misago/services/posting"
import misago from "misago"

export default class extends React.Component {
  onClick = () => {
    posting.open({
      mode: "START_PRIVATE",
      submit: misago.get("PRIVATE_THREADS_API"),

      to: [this.props.profile],
    })
  }

  render() {
    const canMessage = this.props.user.acl.can_start_private_threads
    const isProfileOwner = this.props.user.id === this.props.profile.id

    if (!canMessage || isProfileOwner) return null

    return (
      <button
        className={this.props.className}
        onClick={this.onClick}
        type="button"
      >
        <span className="material-icon">comment</span>
        {pgettext("profile message btn", "Message")}
      </button>
    )
  }
}
