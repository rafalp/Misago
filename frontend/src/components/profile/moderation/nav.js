import React from "react"
import { connect } from "react-redux"
import AvatarControls from "misago/components/profile/moderation/avatar-controls"
import ChangeUsername from "misago/components/profile/moderation/change-username"
import DeleteAccount from "misago/components/profile/moderation/delete-account"
import modal from "misago/services/modal"

let select = function(store) {
  return {
    tick: store.tick,
    user: store.auth,
    profile: store.profile
  }
}

export default class extends React.Component {
  showAvatarDialog = () => {
    modal.show(connect(select)(AvatarControls))
  }

  getAvatarButton() {
    if (this.props.profile.acl.can_moderate_avatar) {
      return (
        <li>
          <button
            type="button"
            className="btn btn-link"
            onClick={this.showAvatarDialog}
          >
            <span className="material-icon">portrait</span>
            {gettext("Avatar controls")}
          </button>
        </li>
      )
    } else {
      return null
    }
  }

  showRenameDialog = () => {
    modal.show(connect(select)(ChangeUsername))
  }

  getRenameButton() {
    if (this.props.profile.acl.can_rename) {
      return (
        <li>
          <button
            type="button"
            className="btn btn-link"
            onClick={this.showRenameDialog}
          >
            <span className="material-icon">credit_card</span>
            {gettext("Change username")}
          </button>
        </li>
      )
    } else {
      return null
    }
  }

  showDeleteDialog = () => {
    modal.show(connect(select)(DeleteAccount))
  }

  getDeleteButton() {
    if (this.props.profile.acl.can_delete) {
      return (
        <li>
          <button
            type="button"
            className="btn btn-link"
            onClick={this.showDeleteDialog}
          >
            <span className="material-icon">clear</span>
            {gettext("Delete account")}
          </button>
        </li>
      )
    } else {
      return null
    }
  }

  render() {
    return (
      <ul
        className="dropdown-menu dropdown-menu-right stick-to-bottom"
        role="menu"
      >
        {this.getAvatarButton()}
        {this.getRenameButton()}
        {this.getDeleteButton()}
      </ul>
    )
  }
}
