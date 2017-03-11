/* jshint ignore:start */
import React from 'react';
import modal from 'misago/services/modal';
import * as moderation from './actions';
import MoveModal from './move';
import SplitModal from './split';

export default function(props) {
  return (
    <ul className="dropdown-menu">
      <Approve {...props} />
      <Merge {...props} />
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
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_approve;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Approve")}
        </button>
      </li>
    );
  }
}

export class Merge extends React.Component {
  onClick = () => {
    moderation.merge(this.props);
  };

  render() {
    if (this.props.selection.length < 2 || !this.props.thread.acl.can_merge_posts) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Merge")}
        </button>
      </li>
    );
  }
}

export class Move extends React.Component {
  onClick = () => {
    modal.show(
      <MoveModal {...this.props} />
    );
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_move;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Move")}
        </button>
      </li>
    );
  }
}

export class Split extends React.Component {
  onClick = () => {
    modal.show(
      <SplitModal {...this.props} />
    );
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_move;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Split")}
        </button>
      </li>
    );
  }
}

export class Protect extends React.Component {
  onClick = () => {
    moderation.protect(this.props);
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_protect;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Protect")}
        </button>
      </li>
    );
  }
}

export class Unprotect extends React.Component {
  onClick = () => {
    moderation.unprotect(this.props);
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_protect;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Unprotect")}
        </button>
      </li>
    );
  }
}

export class Hide extends React.Component {
  onClick = () => {
    moderation.hide(this.props);
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_hide;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Hide")}
        </button>
      </li>
    );
  }
}

export class Unhide extends React.Component {
  onClick = () => {
    moderation.unhide(this.props);
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_unhide;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Unhide")}
        </button>
      </li>
    );
  }
}

export class Delete extends React.Component {
  onClick = () => {
    moderation.remove(this.props);
  };

  render() {
    const isVisible = this.props.selection.find((post) => {
      return post.acl.can_delete;
    });

    if (!isVisible) {
      return null;
    }

    return (
      <li>
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {gettext("Delete")}
        </button>
      </li>
    );
  }
}