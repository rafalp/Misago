import React from 'react'; // jshint ignore:line
import PanelMessage from 'misago/components/panel-message';

export default class extends PanelMessage {
  getHelpText() {
    if (this.props.helpText) {
      /* jshint ignore:start */
      return <p className="help-block">
        {this.props.helpText}
      </p>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="modal-body">
      <div className="message-icon">
        <span className="material-icon">
          {this.props.icon || 'info_outline'}
        </span>
      </div>
      <div className="message-body">
        <p className="lead">
          {this.props.message}
        </p>
        {this.getHelpText()}
        <button
          className="btn btn-default"
          data-dismiss="modal"
          type="button"
        >
          {gettext("Ok")}
        </button>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}