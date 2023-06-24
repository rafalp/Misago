import React from "react"
import AddParticipantModal from "misago/components/add-participant"
import modal from "misago/services/modal"

export default class extends React.Component {
  onClick = () => {
    modal.show(<AddParticipantModal thread={this.props.thread} />)
  }

  render() {
    if (!this.props.thread.acl.can_add_participants) return null

    return (
      <div className="col-xs-12 col-sm-3">
        <button
          className="btn btn-default btn-block"
          onClick={this.onClick}
          type="button"
        >
          <span className="material-icon">person_add</span>
          {pgettext("add participant btn", "Add participant")}
        </button>
      </div>
    )
  }
}
