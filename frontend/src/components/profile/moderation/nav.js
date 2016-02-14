import React from 'react';
import { connect } from 'react-redux'; // jshint ignore:line
import AvatarControls from 'misago/components/profile/moderation/avatar-controls'; // jshint ignore:line
import ChangeUsername from 'misago/components/profile/moderation/change-username'; // jshint ignore:line
import DeleteAccount from 'misago/components/profile/moderation/delete-account'; // jshint ignore:line
import modal from 'misago/services/modal'; // jshint ignore:line

/* jshint ignore:start */
let select = function(store) {
  return {
    tick: store.tick,
    user: store.auth,
    profile: store.profile,
  };
};
/* jshint ignore:end */

export default class extends React.Component {
  /* jshint ignore:start */
  showAvatarDialog = () => {
    modal.show(connect(select)(AvatarControls));
  };
  /* jshint ignore:end */

  getAvatarButton() {
    if (this.props.profile.acl.can_moderate_avatar) {
      /* jshint ignore:start */
      return <li>
        <button type="button" className="btn-link"
                onClick={this.showAvatarDialog}>
          <span className="material-icon">
            portrait
          </span>
          {gettext("Avatar controls")}
        </button>
      </li>
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  /* jshint ignore:start */
  showRenameDialog = () => {
    modal.show(connect(select)(ChangeUsername));
  };
  /* jshint ignore:end */

  getRenameButton() {
    if (this.props.profile.acl.can_rename) {
      /* jshint ignore:start */
      return <li>
        <button type="button" className="btn-link"
                onClick={this.showRenameDialog}>
          <span className="material-icon">
            credit_card
          </span>
          {gettext("Change username")}
        </button>
      </li>
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  /* jshint ignore:start */
  showDeleteDialog = () => {
    modal.show(connect(select)(DeleteAccount));
  };
  /* jshint ignore:end */

  getDeleteButton() {
    if (this.props.profile.acl.can_delete) {
      /* jshint ignore:start */
      return <li>
        <button type="button" className="btn-link"
                onClick={this.showDeleteDialog}>
          <span className="material-icon">
            clear
          </span>
          {gettext("Delete account")}
        </button>
      </li>
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <ul className="dropdown-menu dropdown-menu-right" role="menu">
      {this.getAvatarButton()}
      {this.getRenameButton()}
      {this.getDeleteButton()}
      <li className="divider hidden-md hidden-lg" />
      <li className="dropdown-buttons hidden-md hidden-lg">
        <button type="button" className="btn btn-default btn-block"
                onClick={this.props.toggleNav}>
          <span className="material-icon">
            menu
          </span>
          {gettext("Menu")}
        </button>
      </li>
    </ul>;
    /* jshint ignore:end */
  }
}