import React from 'react';

export class AuthMessage extends React.Component {
  refresh() {
    window.location.reload();
  }

  getMessage() {
    if (this.props.signedIn) {
      return interpolate(
        gettext("You have signed in as %(username)s. Please refresh the page before continuing."),
        {username: this.props.signedIn.username}, true);
    } else if (this.props.signedOut) {
      return interpolate(
        gettext("%(username)s, you have been signed out. Please refresh the page before continuing."),
        {username: this.props.user.username}, true);
    }
  }

  getClassName() {
    if (this.props.signedIn || this.props.signedOut) {
      return "auth-message show";
    } else {
      return "auth-message";
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className={this.getClassName()}>
      <div className="container">
        <p className="lead">{this.getMessage()}</p>
        <p>
          <button type="button" className="btn btn-default"
                  onClick={this.refresh}>
            {gettext("Reload page")}
          </button> <span className="hidden-xs hidden-sm text-muted">
            {gettext("or press F5 key.")}
          </span>
        </p>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

export function select(state) {
  return {
    user: state.auth.user,
    signedIn: state.auth.signedIn,
    signedOut: state.auth.signedOut
  };
}