import React from 'react';
import AvatarCrop from 'misago/components/change-avatar/crop'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line
import fileSize from 'misago/utils/file-size';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'image': null,
      'preview': null,
      'progress': 0,
      'uploaded': null,
    };
  }

  validateFile(image) {
    if (image.size > this.props.options.upload.limit) {
      return interpolate(gettext("Selected file is too big. (%(filesize)s)"), {
        'filesize': fileSize(image.size)
      }, true);
    }

    let invalidTypeMsg = gettext("Selected file type is not supported.");
    if (this.props.options.upload.allowed_mime_types.indexOf(image.type) === -1) {
      return invalidTypeMsg;
    }

    let extensionFound = false;
    let loweredFilename = image.name.toLowerCase();
    this.props.options.upload.allowed_extensions.map(function(extension) {
      if (loweredFilename.substr(extension.length * -1) === extension) {
        extensionFound = true;
      }
    });

    if (!extensionFound) {
      return invalidTypeMsg;
    }

    return false;
  }

  /* jshint ignore:start */
  pickFile = () => {
    document.getElementById('avatar-hidden-upload').click();
  };

  uploadFile = () => {
    let image = document.getElementById('avatar-hidden-upload').files[0];

    let validationError = this.validateFile(image);
    if (validationError) {
      snackbar.error(validationError);
      return;
    }

    this.setState({
      image,
      'preview': URL.createObjectURL(image),
      'progress': 0
    });

    let data = new FormData();
    data.append('avatar', 'upload');
    data.append('image', image);

    ajax.upload(this.props.user.api_url.avatar, data, (progress) => {
      this.setState({
        progress
      });
    }).then((data) => {
      this.setState({
        'options': data,
        'uploaded': data.detail
      });
      snackbar.info(gettext("Your image has been uploaded and you may now crop it."));
    }, (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail);
        this.setState({
          'isLoading': false,
          'image': null,
          'progress': 0
        });
      } else {
        this.props.showError(rejection);
      }
    });
  };
  /* jshint ignore:end */

  getUploadRequirements(options) {
    let extensions = options.allowed_extensions.map(function(extension) {
      return extension.substr(1);
    });

    return interpolate(gettext("%(files)s files smaller than %(limit)s"), {
        'files': extensions.join(', '),
        'limit': fileSize(options.limit)
      }, true);
  }

  getUploadButton() {
    /* jshint ignore:start */
    return <div className="modal-body modal-avatar-upload">
        <Button className="btn-pick-file"
                onClick={this.pickFile}>
          <div className="material-icon">
            input
          </div>
          {gettext("Select file")}
        </Button>
        <p className="text-muted">
          {this.getUploadRequirements(this.props.options.upload)}
        </p>
    </div>;
    /* jshint ignore:end */
  }

  getUploadProgressLabel() {
    return interpolate(gettext("%(progress)s % complete"), {
        'progress': this.state.progress
      }, true);
  }

  getUploadProgress() {
    /* jshint ignore:start */
    return <div className="modal-body modal-avatar-upload">
        <div className="upload-progress">
          <img src={this.state.preview} />

          <div className="progress">
            <div className="progress-bar" role="progressbar"
                 aria-valuenow="{this.state.progress}"
                 aria-valuemin="0" aria-valuemax="100"
                 style={{width: this.state.progress + '%'}}>
              <span className="sr-only">{this.getUploadProgressLabel()}</span>
            </div>
          </div>
        </div>
    </div>;
    /* jshint ignore:end */
  }

  renderUpload() {
    /* jshint ignore:start */
    return <div>
      <input type="file"
             id="avatar-hidden-upload"
             className="hidden-file-upload"
             onChange={this.uploadFile} />
      {this.state.image ? this.getUploadProgress()
                        : this.getUploadButton()}
      <div className="modal-footer">
        <div className="col-md-6 col-md-offset-3">

          <Button onClick={this.props.showIndex}
                  disabled={!!this.state.image}
                  className="btn-default btn-block">
            {gettext("Cancel")}
          </Button>

        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }

  renderCrop() {
    /* jshint ignore:start */
    return <AvatarCrop options={this.state.options}
                       user={this.props.user}
                       upload={this.state.uploaded}
                       onComplete={this.props.onComplete}
                       showError={this.props.showError}
                       showIndex={this.props.showIndex} />;
    /* jshint ignore:end */
  }

  render() {
    /* jshint ignore:start */
    return (this.state.uploaded ? this.renderCrop()
                                : this.renderUpload());
    /* jshint ignore:end */
  }
}