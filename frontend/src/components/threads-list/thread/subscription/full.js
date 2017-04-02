/* jshint ignore:start */
import React from 'react';
import Options from 'misago/components/threads-list/thread/subscription/options';

export default class extends React.Component {
  getIcon() {
    if (this.props.thread.subscription === true) {
      return 'star';
    } else if (this.props.thread.subscription === false) {
      return 'star_half';
    }

    return 'star_border';
  }

  getClassName() {
    if (this.props.thread.subscription === true) {
      return "btn btn-default btn-icon btn-block btn-subscribe btn-subscribe-full dropdown-toggle";
    } else if (this.props.thread.subscription === false) {
      return "btn btn-default btn-icon btn-block btn-subscribe btn-subscribe-half dropdown-toggle";
    }

    return "btn btn-default btn-icon btn-block btn-subscribe dropdown-toggle";
  }

  render() {
    const { moderation, subscription } = this.props.thread;
    const fullwidth = !moderation.length;

    let className = fullwidth ? 'col-xs-12' : 'col-xs-6';
    className += ' hidden-xs hidden-sm';

    return (
      <div className={className}>
        <div className="btn-group btn-group-justified">
          <div className="btn-group">
            <button
              type="button"
              className={this.getClassName()}
              disabled={this.props.disabled}
              data-toggle="dropdown"
              aria-haspopup="true"
              aria-expanded="false"
            >
              <span className="material-icon">
                {this.getIcon()}
              </span>
              <Label
                moderation={moderation}
                subscription={subscription}
              />
            </button>

            <Options
              className="dropdown-menu dropdown-menu-right"
              thread={this.props.thread}
            />

          </div>
        </div>
      </div>
    );
  }
}

export function Label({ moderation, subscription }) {
  if (moderation.length) return null;

  let text = gettext("Disabled");
  if (subscription === true) {
    text = gettext("E-mail");
  } else if (subscription === false) {
    text = gettext("Enabled");
  }

  return (
    <span className="btn-text">
      {text}
    </span>
  );
}