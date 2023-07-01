import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import Loader from "misago/components/modal-loader"
import ModalMessage from "misago/components/modal-message"
import { addNameChange } from "misago/reducers/username-history"
import { updateUsername } from "misago/reducers/users"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"
import * as validators from "misago/utils/validators"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      isLoaded: false,
      isLoading: false,
      error: null,

      username: "",
      validators: {
        username: [validators.usernameContent()],
      },
    }
  }

  componentDidMount() {
    ajax.get(this.props.profile.api.moderate_username).then(
      () => {
        this.setState({
          isLoaded: true,
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
    return ajax.post(this.props.profile.api.moderate_username, {
      username: this.state.username,
    })
  }

  handleSuccess(apiResponse) {
    this.setState({
      username: "",
    })

    store.dispatch(
      addNameChange(apiResponse, this.props.profile, this.props.user)
    )
    store.dispatch(
      updateUsername(this.props.profile, apiResponse.username, apiResponse.slug)
    )

    snackbar.success(
      pgettext("profile username moderation", "Username has been changed.")
    )
  }

  getFormBody() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="modal-body">
          <FormGroup
            label={pgettext(
              "profile username moderation field",
              "New username"
            )}
            for="id_username"
          >
            <input
              type="text"
              id="id_username"
              className="form-control"
              disabled={this.state.isLoading}
              onChange={this.bindInput("username")}
              value={this.state.username}
            />
          </FormGroup>
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-default"
            data-dismiss="modal"
            disabled={this.state.isLoading}
            type="button"
          >
            {pgettext("profile username moderation btn", "Cancel")}
          </button>
          <Button className="btn-primary" loading={this.state.isLoading}>
            {pgettext("profile username moderation btn", "Change username")}
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
      return "modal-dialog modal-message modal-rename-user"
    } else {
      return "modal-dialog modal-rename-user"
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
              {pgettext("profile username moderation title", "Change username")}
            </h4>
          </div>
          {this.getModalBody()}
        </div>
      </div>
    )
  }
}
