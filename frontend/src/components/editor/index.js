// jshint ignore:start
import React from 'react';
import Button from 'misago/components/button';

export default class extends React.Component {
  render() {
    return (
      <div className="editor-border">
        <textarea
          className="form-control"
          rows="7"
        />
        <div className="editor-footer">
          <Button className="btn-primary btn-sm pull-right">
            {this.props.submitLabel || gettext("Post")}
          </Button>
          <Button className="btn-default btn-sm pull-right" onClick={this.props.onClose}>
            {gettext("Cancel")}
          </Button>
        </div>
      </div>
    );
  }
}