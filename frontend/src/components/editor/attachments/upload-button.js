// jshint ignore:start
import React from 'react';
import misago from 'misago';

export default class extends React.Component {
  onClick = () => {
    document.getElementById('editor-upload-field').click();
  };

  render() {
    if (!misago.get('user').acl.max_attachment_size) {
      return null;
    }

    return (
      <button
        className={'btn ' + this.props.className}
        disabled={this.props.disabled}
        onClick={this.onClick}
        title={gettext('Upload file')}
        type="button"
      >
        <span className="material-icon">
          file_upload
        </span>
      </button>
    );
  }
};
