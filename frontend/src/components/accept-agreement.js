import React from "react"
import ajax from "misago/services/ajax"

export default class AcceptAgreement extends React.Component {
  constructor(props) {
    super(props)

    this.state = { submiting: false }
  }

  handleDecline = () => {
    if (this.state.submiting) return

    const confirmation = confirm(
      gettext(
        "Declining will result in immediate deactivation and deletion of your account. This action is not reversible."
      )
    )
    if (!confirmation) return

    this.setState({ submiting: true })

    ajax.post(this.props.api, { accept: false }).then(() => {
      location.reload(true)
    })
  }

  handleAccept = () => {
    if (this.state.submiting) return

    this.setState({ submiting: true })

    ajax.post(this.props.api, { accept: true }).then(() => {
      location.reload(true)
    })
  }

  render() {
    return (
      <div>
        {/* NOTE(Avi): Removed as part of PG-1428 */}
        {/* <button
          className="btn btn-default"
          disabled={this.state.submiting}
          type="buton"
          onClick={this.handleDecline}
        >
          {gettext("Decline")}
        </button> */}
        <button
          className="btn btn-primary"
          disabled={this.state.submiting}
          type="buton"
          onClick={this.handleAccept}
        >
          {gettext("Accept and continue")}
        </button>
      </div>
    )
  }
}
