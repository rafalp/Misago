import React from "react"
import AvatarIndex from "misago/components/change-avatar/index"
import AvatarCrop from "misago/components/change-avatar/crop"
import AvatarUpload from "misago/components/change-avatar/upload"
import AvatarGallery from "misago/components/change-avatar/gallery"
import Loader from "misago/components/modal-loader"
import { updateAvatar } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import store from "misago/services/store"

export class ChangeAvatarError extends React.Component {
  getErrorReason() {
    if (this.props.reason) {
      return <p dangerouslySetInnerHTML={{ __html: this.props.reason }} />
    } else {
      return null
    }
  }

  render() {
    return (
      <div className="modal-body">
        <div className="message-icon">
          <span className="material-icon">remove_circle_outline</span>
        </div>
        <div className="message-body">
          <p className="lead">{this.props.message}</p>
          {this.getErrorReason()}
          <button
            className="btn btn-default"
            data-dismiss="modal"
            type="button"
          >
            {pgettext("avatar modal dismiss", "Ok")}
          </button>
        </div>
      </div>
    )
  }
}

export default class extends React.Component {
  componentDidMount() {
    ajax.get(this.props.user.api.avatar).then(
      (options) => {
        this.setState({
          component: AvatarIndex,
          options: options,
          error: null,
        })
      },
      (rejection) => {
        this.showError(rejection)
      }
    )
  }

  showError = (error) => {
    this.setState({
      error,
    })
  }

  showIndex = () => {
    this.setState({
      component: AvatarIndex,
    })
  }

  showUpload = () => {
    this.setState({
      component: AvatarUpload,
    })
  }

  showCrop = () => {
    this.setState({
      component: AvatarCrop,
    })
  }

  showGallery = () => {
    this.setState({
      component: AvatarGallery,
    })
  }

  completeFlow = (options) => {
    store.dispatch(updateAvatar(this.props.user, options.avatars))

    this.setState({
      component: AvatarIndex,
      options,
    })
  }

  getBody() {
    if (this.state) {
      if (this.state.error) {
        return (
          <ChangeAvatarError
            message={this.state.error.detail}
            reason={this.state.error.reason}
          />
        )
      } else {
        return (
          <this.state.component
            options={this.state.options}
            user={this.props.user}
            onComplete={this.completeFlow}
            showError={this.showError}
            showIndex={this.showIndex}
            showCrop={this.showCrop}
            showUpload={this.showUpload}
            showGallery={this.showGallery}
          />
        )
      }
    } else {
      return <Loader />
    }
  }

  getClassName() {
    if (this.state && this.state.error) {
      return "modal-dialog modal-message modal-change-avatar"
    } else {
      return "modal-dialog modal-change-avatar"
    }
  }

  render() {
    return (
      <div className={this.getClassName()} role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              type="button"
              className="close"
              data-dismiss="modal"
              aria-label={pgettext("modal", "Close")}
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">
              {pgettext("avatar modal title", "Change your avatar")}
            </h4>
          </div>

          {this.getBody()}
        </div>
      </div>
    )
  }
}

export function select(state) {
  return {
    user: state.auth.user,
  }
}
