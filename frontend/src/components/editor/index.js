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
          <Button
            className="btn-default btn-sm pull-right"
            disabled={this.props.loading}
            onClick={this.props.onClose}
          >
            {gettext("Cancel")}
          </Button>
        </div>
      </div>
    );
  }
}