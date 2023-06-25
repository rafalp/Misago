import React from "react"
import { connect } from "react-redux"
import AvatarControls from "misago/components/profile/moderation/avatar-controls"
import ChangeUsername from "misago/components/profile/moderation/change-username"
import DeleteAccount from "misago/components/profile/moderation/delete-account"
import modal from "misago/services/modal"

let select = function (store) {
  return {
    tick: store.tick,
    user: store.auth,
    profile: store.profile,
  }
}

export default class extends React.Component {
  showAvatarDialog = () => {
    modal.show(connect(select)(AvatarControls))
  }

  showRenameDialog = () => {
    modal.show(connect(select)(ChangeUsername))
  }

  showDeleteDialog = () => {
    modal.show(connect(select)(DeleteAccount))
  }

  render() {
    const { moderation } = this.props

    return (
      <ul className="dropdown-menu dropdown-menu-right" role="menu">
        {!!moderation.avatar && (
          <li>
            <button
              type="button"
              className="btn btn-link"
              onClick={this.showAvatarDialog}
            >
              <span className="material-icon">portrait</span>
              {pgettext("profile moderation menu", "Avatar controls")}
            </button>
          </li>
        )}
        {!!moderation.rename && (
          <li>
            <button
              type="button"
              className="btn btn-link"
              onClick={this.showRenameDialog}
            >
              <span className="material-icon">credit_card</span>
              {pgettext("profile moderation menu", "Change username")}
            </button>
          </li>
        )}
        {!!moderation.delete && (
          <li>
            <button
              type="button"
              className="btn btn-link"
              onClick={this.showDeleteDialog}
            >
              <span className="material-icon">clear</span>
              {pgettext("profile moderation menu", "Delete account")}
            </button>
          </li>
        )}
      </ul>
    )
  }
}
