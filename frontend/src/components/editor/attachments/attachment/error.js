// jshint ignore:start
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';

const STRONG = '<strong>%(name)s</strong>';

export default class extends React.Component {
  onClick = () => {
    const filteredAttachments = this.props.attachments.filter((item) => {
      return item.key !== this.props.item.key;
    });
    this.props.onAttachmentsChange(filteredAttachments);
  };

  render() {
    const filename = interpolate(STRONG, {
      name: escapeHtml(this.props.item.filename)
    }, true);

    const title = interpolate(gettext("Error uploading %(filename)s"), {
      filename,
      progress: this.props.item.progress + '%'
    }, true);

    return (
      <li className="editor-attachment-error">
        <div className="editor-attachment-error-icon">
          <span className="material-icon">
            warning
          </span>
        </div>
        <div className="editor-attachment-error-message">
          <h4 dangerouslySetInnerHTML={{__html: title + ':'}} />
          <p>{this.props.item.error}</p>
          <button
            className="btn btn-default btn-sm"
            onClick={this.onClick}
            type="button"
          >
            {gettext("Dismiss")}
          </button>
        </div>
      </li>
    );
  }
};