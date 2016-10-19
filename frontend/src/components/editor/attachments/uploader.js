// jshint ignore:start
import React from 'react';
import moment from 'moment';
import misago from 'misago';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  onChange = (event) => {
    const file = event.target.files[0];
    if (!file) {
      return;
    }

    let upload = {
      id: null,
      key: getRandomKey(),
      progress: 0,
      error: null,
      filename: file.name
    };

    this.props.onAttachmentsChange([upload].concat(this.props.attachments));

    const data = new FormData();
    data.append('upload', file);

    ajax.upload(misago.get('ATTACHMENTS_API'), data, (progress) => {
      upload.progress = progress;
      this.props.onAttachmentsChange(this.props.attachments.concat());
    }).then((data) => {
      data.uploaded_on = moment(data.uploaded_on);
      Object.assign(upload, data);
      this.props.onAttachmentsChange(this.props.attachments.concat());
    }, (rejection) => {
      if (rejection.status === 400) {
        upload.error = rejection.detail;
        this.props.onAttachmentsChange(this.props.attachments.concat());
      } else {
        snackbar.apiError(rejection);
      }
    });
  };

  render() {
    return (
      <input
        id="editor-upload-field"
        onChange={this.onChange}
        type="file"
      />
    );
  }
};

export function getRandomKey() {
  return 'upld-' + Math.round(new Date().getTime());
}