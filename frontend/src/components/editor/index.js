// jshint ignore:start
import React from 'react';
import Button from 'misago/components/button';

export default class extends React.Component {
  render() {
    return (
      <div className="editor-border">
        <textarea
          className="form-control"
          disabled={this.props.loading}
          onChange={this.props.onChange}
          rows="7"
          value={this.props.value}
        />
        <div className="editor-footer">
          <Button
            className="btn-primary btn-sm pull-right"
            loading={this.props.loading}
          >
            {this.props.submitLabel || gettext("Post")}
          </Button>
          <button
            className="btn btn-default btn-sm pull-right"
            disabled={this.props.loading}
            onClick={this.props.onCancel}
            type="button"
          >
            {gettext("Cancel")}
          </button>
          <Protect
            canProtect={this.props.canProtect}
            disabled={this.props.loading}
            onProtect={this.props.onProtect}
            onUnprotect={this.props.onUnprotect}
            protect={this.props.protect}
          />
        </div>
      </div>
    );
  }
}

export function Protect(props) {
  if (props.canProtect) {
    return (
      <button
        className="btn btn-default btn-sm pull-right"
        disabled={props.disabled}
        onClick={props.protect ? props.onUnprotect : props.onProtect}
        title={props.protect ? gettext('Protected') : gettext('Protect')}
        type="button"
      >
        <span className="material-icon">
          {props.protect ? 'lock' : 'lock_outline'}
        </span>
      </button>
    );
  } else {
    return null;
  }
}