import React from "react"
import Avatar from "misago/components/avatar"
import Button from "misago/components/button"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      deviceRatio: 1,
    }
  }

  getAvatarSize() {
    if (this.props.upload) {
      return this.props.options.crop_tmp.size
    } else {
      return this.props.options.crop_src.size
    }
  }

  getImagePath() {
    if (this.props.upload) {
      return this.props.dataUrl
    } else {
      return this.props.options.crop_src.url
    }
  }

  componentDidMount() {
    let cropit = $(".crop-form")
    let cropperWidth = this.getAvatarSize()

    const initialWidth = cropit.width()
    while (initialWidth < cropperWidth) {
      cropperWidth = cropperWidth / 2
    }

    const deviceRatio = this.getAvatarSize() / cropperWidth

    cropit.width(cropperWidth)

    cropit.cropit({
      width: cropperWidth,
      height: cropperWidth,
      exportZoom: deviceRatio,
      imageState: {
        src: this.getImagePath(),
      },
      onImageLoaded: () => {
        if (this.props.upload) {
          // center uploaded image
          let zoomLevel = cropit.cropit("zoom")
          let imageSize = cropit.cropit("imageSize")

          // is it wider than taller?
          if (imageSize.width > imageSize.height) {
            let displayedWidth = imageSize.width * zoomLevel
            let offsetX = (displayedWidth - this.getAvatarSize()) / -2

            cropit.cropit("offset", {
              x: offsetX,
              y: 0,
            })
          } else if (imageSize.width < imageSize.height) {
            let displayedHeight = imageSize.height * zoomLevel
            let offsetY = (displayedHeight - this.getAvatarSize()) / -2

            cropit.cropit("offset", {
              x: 0,
              y: offsetY,
            })
          } else {
            cropit.cropit("offset", {
              x: 0,
              y: 0,
            })
          }
        } else {
          // use preserved crop
          let crop = this.props.options.crop_src.crop

          if (crop) {
            cropit.cropit("zoom", crop.zoom)
            cropit.cropit("offset", {
              x: crop.x,
              y: crop.y,
            })
          }
        }
      },
    })
  }

  componentWillUnmount() {
    $(".crop-form").cropit("disable")
  }

  cropAvatar = () => {
    if (this.state.isLoading) {
      return false
    }

    this.setState({
      isLoading: true,
    })

    let avatarType = this.props.upload ? "crop_tmp" : "crop_src"
    let cropit = $(".crop-form")

    const deviceRatio = cropit.cropit("exportZoom")
    const cropitOffset = cropit.cropit("offset")

    ajax
      .post(this.props.user.api.avatar, {
        avatar: avatarType,
        crop: {
          offset: {
            x: cropitOffset.x * deviceRatio,
            y: cropitOffset.y * deviceRatio,
          },
          zoom: cropit.cropit("zoom") * deviceRatio,
        },
      })
      .then(
        (data) => {
          this.props.onComplete(data)
          snackbar.success(data.detail)
        },
        (rejection) => {
          if (rejection.status === 400) {
            snackbar.error(rejection.detail)
            this.setState({
              isLoading: false,
            })
          } else {
            this.props.showError(rejection)
          }
        }
      )
  }

  render() {
    return (
      <div>
        <div className="modal-body modal-avatar-crop">
          <div className="crop-form">
            <div className="cropit-preview" />
            <input type="range" className="cropit-image-zoom-input" />
          </div>
        </div>
        <div className="modal-footer">
          <div className="col-md-6 col-md-offset-3">
            <Button
              onClick={this.cropAvatar}
              loading={this.state.isLoading}
              className="btn-primary btn-block"
            >
              {this.props.upload
                ? pgettext("avatar crop modal btn", "Set avatar")
                : pgettext("avatar crop modal btn", "Crop image")}
            </Button>

            <Button
              onClick={this.props.showIndex}
              disabled={this.state.isLoading}
              className="btn-default btn-block"
            >
              {pgettext("avatar crop modal btn", "Cancel")}
            </Button>
          </div>
        </div>
      </div>
    )
  }
}
