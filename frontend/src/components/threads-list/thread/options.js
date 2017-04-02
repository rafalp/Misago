/* jshint ignore:start */
import React from 'react';
import SubscriptionCompact from 'misago/components/threads-list/thread/subscription/compact';
import SubscriptionFull from 'misago/components/threads-list/thread/subscription/full';
import * as select from 'misago/reducers/selection';
import store from 'misago/services/store';

export function Options({ display, disabled, isSelected, thread }) {
  if (!display) return null;

  let className = 'col-sm-2 col-md-2 hidden-xs';
  if (thread.moderation.length) {
    className = 'col-sm-3 col-md-2 hidden-xs';
  }

  return (
    <div className={className}>
      <div className="row thread-options">
        <SubscriptionFull
          thread={thread}
          disabled={disabled}
        />
        <SubscriptionCompact
          thread={thread}
          disabled={disabled}
        />
        <Checkbox
          thread={thread}
          disabled={disabled}
          isSelected={isSelected}
         />
      </div>
    </div>
  );
}

export function OptionsXs({ display, disabled, isSelected, thread }) {
  if (!display) return null;

  let className = ''
  if (thread.moderation.length) {
    className += 'col-xs-6';
  } else {
    className += 'col-xs-3';
  }
  className += ' visible-xs-block thread-options-xs';

  return (
    <div className={className}>
      <div className="row thread-options">
        <SubscriptionFull
          thread={thread}
          disabled={disabled}
        />
        <SubscriptionCompact
          thread={thread}
          disabled={disabled}
        />
        <Checkbox
          thread={thread}
          disabled={disabled}
          isSelected={isSelected}
         />
      </div>
    </div>
  );
}

export class Checkbox extends React.Component {
  toggleSelection = () => {
    store.dispatch(select.item(this.props.thread.id));
  };

  render() {
    const { disabled, isSelected, thread } = this.props;

    if (!thread.moderation.length) return null;

    return (
      <div className="col-xs-6">
        <button
          className="btn btn-default btn-icon btn-block"
          onClick={this.toggleSelection}
          disabled={disabled}
        >
          <span className="material-icon">
            {isSelected ? 'check_box' : 'check_box_outline_blank'}
          </span>
        </button>
      </div>
    );
  }
}