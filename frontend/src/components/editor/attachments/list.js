// jshint ignore:start
import React from 'react';
import escapeHtml from 'misago/utils/escape-html';
import misago from 'misago';

const STRONG = '<strong>%(name)s</strong>';

export default function(props) {
  return (
    <ul className="list-unstyled editor-attachments-list">
      {props.attachments.map((item) => {
        if (item.id) {
          return (
            <Attachment item={item} key={item.id} {...props} />
          );
        } else if (item.error) {
          return (
            <AttachmentError item={item} key={item.key} {...props} />
          );
        } else {
          return (
            <AttachmentUpload item={item} key={item.key} {...props} />
          );
        }
      })}
    </ul>
  );
};

export class Attachment extends React.Component {
  render() {
    return (
      <li className="editor-attachment-ready">
        <a
          href={this.props.item.url.index}
          target="_blank"
        >
          {this.props.item.filename}
        </a>
      </li>
    );
  }
};

export class AttachmentError extends React.Component {
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

export function AttachmentUpload(props) {
  const filename = interpolate(STRONG, {
    name: escapeHtml(props.item.filename)
  }, true);

  const message = interpolate(gettext("Uploading %(filename)s... %(progress)s"), {
    filename,
    progress: props.item.progress + '%'
  }, true);

  return (
    <li className="editor-attachment-upload">
      <div className="editor-attachment-progress-bar">
        <div
          className="editor-attachment-progress"
          style={{width: props.item.progress + '%'}}
        />
      </div>
      <p
        className="editor-attachment-upload-message"
        dangerouslySetInnerHTML={{__html: message}}
      />
    </li>
  );
};