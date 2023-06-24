import React from "react"
import Avatar from "misago/components/avatar"
import Button from "misago/components/button"
import Loader from "misago/components/loader"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
    }
  }

  callApi(avatarType) {
    if (this.state.isLoading) {
      return false
    }

    this.setState({
      isLoading: true,
    })

    ajax
      .post(this.props.user.api.avatar, {
        avatar: avatarType,
      })
      .then(
        (response) => {
          this.setState({
            isLoading: false,
          })

          snackbar.success(response.detail)
          this.props.onComplete(response)
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

  setGravatar = () => {
    this.callApi("gravatar")
  }

  setGenerated = () => {
    this.callApi("generated")
  }

  getGravatarButton() {
    if (this.props.options.gravatar) {
      return (
        <Button
          onClick={this.setGravatar}
          disabled={this.state.isLoading}
          className="btn-default btn-block btn-avatar-gravatar"
        >
          {pgettext("avatar modal btn", "Download my Gravatar")}
        </Button>
      )
    } else {
      return null
    }
  }

  getCropButton() {
    if (!this.props.options.crop_src) return null

    return (
      <Button
        className="btn-default btn-block btn-avatar-crop"
        disabled={this.state.isLoading}
        onClick={this.props.showCrop}
      >
        {pgettext("avatar modal btn", "Re-crop uploaded image")}
      </Button>
    )
  }

  getUploadButton() {
    if (!this.props.options.upload) return null

    return (
      <Button
        className="btn-default btn-block btn-avatar-upload"
        disabled={this.state.isLoading}
        onClick={this.props.showUpload}
      >
        {pgettext("avatar modal btn", "Upload new image")}
      </Button>
    )
  }

  getGalleryButton() {
    if (!this.props.options.galleries) return null

    return (
      <Button
        className="btn-default btn-block btn-avatar-gallery"
        disabled={this.state.isLoading}
        onClick={this.props.showGallery}
      >
        {pgettext("avatar modal btn", "Pick avatar from gallery")}
      </Button>
    )
  }

  getAvatarPreview() {
    let userPeview = {
      id: this.props.user.id,
      avatars: this.props.options.avatars,
    }

    if (this.state.isLoading) {
      return (
        <div className="avatar-preview preview-loading">
          <Avatar size="200" user={userPeview} />
          <Loader />
        </div>
      )
    }

    return (
      <div className="avatar-preview">
        <Avatar size="200" user={userPeview} />
      </div>
    )
  }

  render() {
    return (
      <div className="modal-body modal-avatar-index">
        <div className="row">
          <div className="col-md-5">{this.getAvatarPreview()}</div>
          <div className="col-md-7">
            {this.getGravatarButton()}

            <Button
              onClick={this.setGenerated}
              disabled={this.state.isLoading}
              className="btn-default btn-block btn-avatar-generate"
            >
              {pgettext("avatar modal btn", "Generate my individual avatar")}
            </Button>

            {this.getCropButton()}
            {this.getUploadButton()}
            {this.getGalleryButton()}
          </div>
        </div>
      </div>
    )
  }
}
