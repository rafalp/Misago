import React from "react"

export default class extends React.Component {
  refresh() {
    window.location.reload()
  }

  getMessage() {
    if (this.props.signedIn) {
      return interpolate(
        pgettext(
          "auth message",
          "You have signed in as %(username)s. Please refresh the page before continuing."
        ),
        { username: this.props.signedIn.username },
        true
      )
    } else if (this.props.signedOut) {
      return interpolate(
        pgettext(
          "auth message",
          "%(username)s, you have been signed out. Please refresh the page before continuing."
        ),
        { username: this.props.user.username },
        true
      )
    }
  }

  render() {
    let className = "auth-message"
    if (this.props.signedIn || this.props.signedOut) {
      className += " show"
    }

    return (
      <div className={className}>
        <div className="container">
          <p className="lead">{this.getMessage()}</p>
          <p>
            <button
              className="btn btn-default"
              type="button"
              onClick={this.refresh}
            >
              {pgettext("auth message", "Reload page")}
            </button>
            <span className="hidden-xs hidden-sm">
              {" " + pgettext("auth message", "or press F5 key.")}
            </span>
          </p>
        </div>
      </div>
    )
  }
}

export function select(state) {
  return {
    user: state.auth.user,
    signedIn: state.auth.signedIn,
    signedOut: state.auth.signedOut,
  }
}
