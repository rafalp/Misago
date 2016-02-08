import React from 'react';

export default class extends React.Component {
  getHelpText() {
    if (this.props.options.next_on) {
      return interpolate(
          gettext("You will be able to change your username %(next_change)s."),
          {'next_change': this.props.options.next_on.fromNow()}, true);
    } else {
      return gettext("You have used up available name changes.");
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="panel panel-default panel-form">
      <div className="panel-heading">
        <h3 className="panel-title">{gettext("Change username")}</h3>
      </div>
      <div className="panel-body panel-message-body">

        <div className="message-icon">
          <span className="material-icon">
            info_outline
          </span>
        </div>
        <div className="message-body">
          <p className="lead">
            {gettext("You can't change your username at the moment.")}
          </p>
          <p className="help-block">
            {this.getHelpText()}
          </p>
        </div>

      </div>
    </div>;
    /* jshint ignore:end */
  }
}
