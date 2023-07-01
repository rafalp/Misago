import React from "react"
import ajax from "misago/services/ajax"

export default class AcceptAgreement extends React.Component {
  constructor(props) {
    super(props)

    this.state = { submiting: false }
  }

  handleDecline = () => {
    if (this.state.submiting) return

    const confirmation = window.confirm(
      pgettext(
        "accept agreement prompt",
        "Declining will result in immediate deactivation and deletion of your account. This action is not reversible."
      )
    )
    if (!confirmation) return

    this.setState({ submiting: true })

    ajax.post(this.props.api, { accept: false }).then(() => {
      window.location.reload(true)
    })
  }

  handleAccept = () => {
    if (this.state.submiting) return

    this.setState({ submiting: true })

    ajax.post(this.props.api, { accept: true }).then(() => {
      window.location.reload(true)
    })
  }

  render() {
    return (
      <div>
        <button
          className="btn btn-default"
          disabled={this.state.submiting}
          type="buton"
          onClick={this.handleDecline}
        >
          {pgettext("accept agreement choice", "Decline")}
        </button>
        <button
          className="btn btn-primary"
          disabled={this.state.submiting}
          type="buton"
          onClick={this.handleAccept}
        >
          {pgettext("accept agreement choice", "Accept and continue")}
        </button>
      </div>
    )
  }
}
