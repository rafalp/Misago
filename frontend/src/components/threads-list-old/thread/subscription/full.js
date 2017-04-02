import React from 'react';
import Options from 'misago/components/threads-list/thread/subscription/options'; // jshint ignore:line

export default class extends React.Component {
  getIcon() {
    if (this.props.thread.subscription === true) {
      return 'star';
    } else if (this.props.thread.subscription === false) {
      return 'star_half';
    } else {
      return 'star_border';
    }
  }

  getLegend() {
    if (this.props.thread.subscription === true) {
      return gettext("E-mail");
    } else if (this.props.thread.subscription === false) {
      return gettext("Enabled");
    } else {
      return gettext("Disabled");
    }
  }

  getClassName() {
    if (this.props.thread.subscription === true) {
      return "btn btn-default btn-subscribe btn-subscribe-full dropdown-toggle";
    } else if (this.props.thread.subscription === false) {
      return "btn btn-default btn-subscribe btn-subscribe-half dropdown-toggle";
    } else {
      return "btn btn-default btn-subscribe dropdown-toggle";
    }
  }

  render() {
    /* jshint ignore:start */
    return <li className="hidden-xs hidden-sm">
      <div className="btn-group">
        <button type="button"
                className={this.getClassName()}
                disabled={this.props.disabled}
                data-toggle="dropdown"
                aria-haspopup="true"
                aria-expanded="false">
          <span className="material-icon">
            {this.getIcon()}
          </span>
          <span className="icon-legend">
            {this.getLegend()}
          </span>
        </button>

        <Options className="dropdown-menu dropdown-menu-right"
                 thread={this.props.thread} />

      </div>
    </li>;
    /* jshint ignore:end */
  }
}