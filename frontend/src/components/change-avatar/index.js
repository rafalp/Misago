import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import Loader from 'misago/components/loader'; // jshint ignore:line
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'isLoading': false
    };
  }

  callApi(avatarType) {
    if (this.state.isLoading) {
      return false;
    }

    this.setState({
      'isLoading': true
    });

    ajax.post(this.props.user.api_url.avatar, {
      avatar: avatarType
    }).then((response) => {
      this.setState({
        'isLoading': false
      });

      snackbar.success(response.detail);
      this.props.onComplete(response.avatar_hash, response.options);
    }, (rejection) => {
      if (rejection.status === 400) {
        snackbar.error(rejection.detail);
        this.setState({
          'isLoading': false
        });
      } else {
        this.props.showError(rejection);
      }
    });
  }

  /* jshint ignore:start */
  setGravatar = () => {
    this.callApi('gravatar');
  };

  setGenerated = () => {
    this.callApi('generated');
  };
  /* jshint ignore:end */

  getGravatarButton() {
    if (this.props.options.gravatar) {
      /* jshint ignore:start */
      return <Button onClick={this.setGravatar}
              disabled={this.state.isLoading}
              className="btn-default btn-block btn-avatar-gravatar">
        {gettext("Download my Gravatar")}
      </Button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getCropButton() {
    if (this.props.options.crop_org) {
      /* jshint ignore:start */
      return <Button onClick={this.props.showCrop}
              disabled={this.state.isLoading}
              className="btn-default btn-block btn-avatar-crop">
        {gettext("Re-crop uploaded image")}
      </Button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getUploadButton() {
    if (this.props.options.upload) {
      /* jshint ignore:start */
      return <Button onClick={this.props.showUpload}
              disabled={this.state.isLoading}
              className="btn-default btn-block btn-avatar-upload">
        {gettext("Upload new image")}
      </Button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getGalleryButton() {
    if (this.props.options.galleries) {
      /* jshint ignore:start */
      return <Button onClick={this.props.showGallery}
              disabled={this.state.isLoading}
              className="btn-default btn-block btn-avatar-gallery">
        {gettext("Pick avatar from gallery")}
      </Button>;
      /* jshint ignore:end */
    } else {
      return null;
    }
  }

  getAvatarPreview() {
    if (this.state.isLoading) {
      /* jshint ignore:start */
      return <div className="avatar-preview preview-loading">
        <Avatar user={this.props.user} size="200" />
        <Loader />
      </div>;
      /* jshint ignore:end */
    } else {
      /* jshint ignore:start */
      return <div className="avatar-preview">
        <Avatar user={this.props.user} size="200" />
      </div>;
      /* jshint ignore:end */
    }
  }

  render() {
    /* jshint ignore:start */
    return <div className="modal-body modal-avatar-index">
      <div className="row">
        <div className="col-md-5">

          {this.getAvatarPreview()}

        </div>
        <div className="col-md-7">

          {this.getGravatarButton()}

          <Button onClick={this.setGenerated}
                  disabled={this.state.isLoading}
                  className="btn-default btn-block btn-avatar-generate">
            {gettext("Generate my individual avatar")}
          </Button>

          {this.getCropButton()}
          {this.getUploadButton()}
          {this.getGalleryButton()}

        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}