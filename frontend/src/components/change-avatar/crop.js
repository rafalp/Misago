import React from 'react';
import Avatar from 'misago/components/avatar'; // jshint ignore:line
import Button from 'misago/components/button'; // jshint ignore:line
import ajax from 'misago/services/ajax'; // jshint ignore:line
import snackbar from 'misago/services/snackbar'; // jshint ignore:line

const BASE_URL = $('base').attr('href') + 'user-avatar';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      'isLoading': false
    };
  }

  getAvatarSize() {
    if (this.props.upload) {
      return this.props.options.crop_tmp.size;
    } else {
      return this.props.options.crop_org.size;
    }
  }

  getAvatarSecret() {
    if (this.props.upload) {
      return this.props.options.crop_tmp.secret;
    } else {
      return this.props.options.crop_org.secret;
    }
  }

  getAvatarHash() {
    return this.props.upload || this.props.user.avatar_hash;
  }

  getImagePath() {
    return [
      BASE_URL,
      this.getAvatarSecret() + ':' + this.getAvatarHash(),
      this.props.user.id + '.png'
    ].join('/');
  }

  componentDidMount() {
    let cropit = $('.crop-form');
    cropit.width(this.getAvatarSize());

    cropit.cropit({
      'width': this.getAvatarSize(),
      'height': this.getAvatarSize(),
      'imageState': {
        'src': this.getImagePath()
      },
      onImageLoaded: () => {
        if (this.props.upload) {
          // center uploaded image
          let zoomLevel = cropit.cropit('zoom');
          let imageSize = cropit.cropit('imageSize');

          // is it wider than taller?
          if (imageSize.width > imageSize.height) {
            let displayedWidth = (imageSize.width * zoomLevel);
            let offsetX = (displayedWidth - this.getAvatarSize()) / -2;

            cropit.cropit('offset', {
              'x': offsetX,
              'y': 0
            });
          } else if (imageSize.width < imageSize.height) {
            let displayedHeight = (imageSize.height * zoomLevel);
            let offsetY = (displayedHeight - this.getAvatarSize()) / -2;

            cropit.cropit('offset', {
              'x': 0,
              'y': offsetY
            });
          }
        } else {
          // use preserved crop
          let crop = this.props.options.crop_org.crop;
          if (crop) {
            cropit.cropit('zoom', crop.zoom);
            cropit.cropit('offset', {
              'x': crop.x,
              'y': crop.y
            });
          }
        }
      }
    });
  }

  componentWillUnmount() {
    $('.crop-form').cropit('disable');
  }

  /* jshint ignore:start */
  cropAvatar = () => {
    if (this.state.isLoading) {
      return false;
    }

    this.setState({
      'isLoading': true
    });

    let avatarType = this.props.upload ? 'crop_tmp' : 'crop_org';
    let cropit = $('.crop-form');

    ajax.post(this.props.user.api_url.avatar, {
      'avatar': avatarType,
      'crop': {
        'offset': cropit.cropit('offset'),
        'zoom': cropit.cropit('zoom')
      }
    }).then((data) => {
      this.props.onComplete(data.avatar_hash, data.options);
      snackbar.success(data.detail);
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
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    return <div>
      <div className="modal-body modal-avatar-crop">
        <div className="crop-form">
          <div className="cropit-image-preview"></div>
          <input type="range" className="cropit-image-zoom-input" />
        </div>
      </div>
      <div className="modal-footer">
        <div className="col-md-6 col-md-offset-3">

          <Button onClick={this.cropAvatar}
                  loading={this.state.isLoading}
                  className="btn-primary btn-block">
            {this.props.upload ? gettext("Set avatar")
                               : gettext("Crop image")}
          </Button>

          <Button onClick={this.props.showIndex}
                  disabled={this.state.isLoading}
                  className="btn-default btn-block">
            {gettext("Cancel")}
          </Button>

        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}