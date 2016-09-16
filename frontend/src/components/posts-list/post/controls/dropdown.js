/* jshint ignore:start */
import React from 'react';
import modal from 'misago/services/modal';
import * as moderation from './actions';
import MoveModal from './move';
import SplitModal from './split';

export default function(props) {
  return (
    <ul className="dropdown-menu dropdown-menu-right">
      <Approve {...props} />
      <Move {...props} />
      <Split {...props} />
      <Protect {...props} />
      <Unprotect {...props} />
      <Hide {...props} />
      <Unhide {...props} />
      <Delete {...props} />
    </ul>
  );
}

export class Approve extends React.Component {
  onClick = () => {
    moderation.approve(this.props);
  };

  render() {
    if (this.props.post.acl.can_approve && this.props.post.is_unapproved) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Approve")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Move extends React.Component {
  onClick = () => {
    modal.show(
      <MoveModal {...this.props} />
    );
  };

  render() {
    if (this.props.post.acl.can_move) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Move")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Split extends React.Component {
  onClick = () => {
    modal.show(
      <SplitModal {...this.props} />
    );
  };

  render() {
    if (this.props.post.acl.can_move) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Split")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Protect extends React.Component {
  onClick = () => {
    moderation.protect(this.props);
  };

  render() {
    if (this.props.post.acl.can_protect && !this.props.post.is_protected) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Protect")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Unprotect extends React.Component {
  onClick = () => {
    moderation.unprotect(this.props);
  };

  render() {
    if (this.props.post.acl.can_protect && this.props.post.is_protected) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Remove protection")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Hide extends React.Component {
  onClick = () => {
    moderation.hide(this.props);
  };

  render() {
    if (this.props.post.acl.can_hide && !this.props.post.is_hidden) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Hide")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Unhide extends React.Component {
  onClick = () => {
    moderation.unhide(this.props);
  };

  render() {
    if (this.props.post.acl.can_unhide && this.props.post.is_hidden) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Unhide")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}

export class Delete extends React.Component {
  onClick = () => {
    moderation.remove(this.props);
  };

  render() {
    if (this.props.post.acl.can_delete) {
      return (
        <li>
          <button type="button" className="btn btn-link" onClick={this.onClick}>
            {gettext("Delete")}
          </button>
        </li>
      );
    } else {
      return null;
    }
  }
}