import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import Loader from "misago/components/modal-loader"
import YesNoSwitch from "misago/components/yes-no-switch"
import ModalMessage from "misago/components/modal-message"
import { updateAvatar } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoaded: false,
      isLoading: false,
      error: null,

      is_avatar_locked: "",
      avatar_lock_user_message: "",
      avatar_lock_staff_message: "",
    }
  }

  componentDidMount() {
    ajax.get(this.props.profile.api.moderate_avatar).then(
      (options) => {
        this.setState({
          isLoaded: true,

          is_avatar_locked: options.is_avatar_locked,
          avatar_lock_user_message: options.avatar_lock_user_message || "",
          avatar_lock_staff_message: options.avatar_lock_staff_message || "",
        })
      },
      (rejection) => {
        this.setState({
          isLoaded: true,
          error: rejection.detail,
        })
      }
    )
  }

  clean() {
    if (this.isValid()) {
      return true
    } else {
      snackbar.error(this.validate().username[0])
      return false
    }
  }

  send() {
    return ajax.post(this.props.profile.api.moderate_avatar, {
      is_avatar_locked: this.state.is_avatar_locked,
      avatar_lock_user_message: this.state.avatar_lock_user_message,
      avatar_lock_staff_message: this.state.avatar_lock_staff_message,
    })
  }

  handleSuccess(apiResponse) {
    store.dispatch(updateAvatar(this.props.profile, apiResponse.avatar_hash))
    snackbar.success(
      pgettext(
        "profile avatar moderation",
        "Avatar controls have been changed."
      )
    )
  }

  getFormBody() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="modal-body">
          <FormGroup
            label={pgettext("profile avatar moderation field", "Lock avatar")}
            helpText={pgettext(
              "profile avatar moderation field",
              "Locking user avatar will prohibit user from changing his avatar and will reset his/her avatar to default one."
            )}
            for="id_is_avatar_locked"
          >
            <YesNoSwitch
              id="id_is_avatar_locked"
              disabled={this.state.isLoading}
              iconOn="lock_outline"
              iconOff="lock_open"
              labelOn={pgettext(
                "profile avatar moderation field",
                "Disallow user from changing avatar"
              )}
              labelOff={pgettext(
                "profile avatar moderation field",
                "Allow user to change avatar"
              )}
              onChange={this.bindInput("is_avatar_locked")}
              value={this.state.is_avatar_locked}
            />
          </FormGroup>

          <FormGroup
            label={pgettext("profile avatar moderation field", "User message")}
            helpText={pgettext(
              "profile avatar moderation field",
              "Optional message for user explaining why they are prohibited from changing their avatar."
            )}
            for="id_avatar_lock_user_message"
          >
            <textarea
              id="id_avatar_lock_user_message"
              className="form-control"
              rows="4"
              disabled={this.state.isLoading}
              onChange={this.bindInput("avatar_lock_user_message")}
              value={this.state.avatar_lock_user_message}
            />
          </FormGroup>

          <FormGroup
            label={pgettext("profile avatar moderation field", "Staff message")}
            helpText={pgettext(
              "profile avatar moderation field",
              "Optional message for forum team members explaining why the user is prohibited form changing their avatar."
            )}
            for="id_avatar_lock_staff_message"
          >
            <textarea
              id="id_avatar_lock_staff_message"
              className="form-control"
              rows="4"
              disabled={this.state.isLoading}
              onChange={this.bindInput("avatar_lock_staff_message")}
              value={this.state.avatar_lock_staff_message}
            />
          </FormGroup>
        </div>
        <div className="modal-footer">
          <button
            type="button"
            className="btn btn-default"
            data-dismiss="modal"
          >
            {pgettext("profile avatar moderation btn", "Close")}
          </button>
          <Button className="btn-primary" loading={this.state.isLoading}>
            {pgettext("profile avatar moderation btn", "Save changes")}
          </Button>
        </div>
      </form>
    )
  }

  getModalBody() {
    if (this.state.error) {
      return (
        <ModalMessage icon="remove_circle_outline" message={this.state.error} />
      )
    } else if (this.state.isLoaded) {
      return this.getFormBody()
    } else {
      return <Loader />
    }
  }

  getClassName() {
    if (this.state.error) {
      return "modal-dialog modal-message modal-avatar-controls"
    } else {
      return "modal-dialog modal-avatar-controls"
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
              {pgettext("profile avatar moderation title", "Avatar controls")}
            </h4>
          </div>
          {this.getModalBody()}
        </div>
      </div>
    )
  }
}
