import React from "react"
import Button from "misago/components/button"
import Form from "misago/components/form"
import FormGroup from "misago/components/form-group"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import * as validators from "misago/utils/validators"

export default class extends Form {
  constructor(props) {
    super(props)

    this.state = {
      username: "",

      validators: {
        username: [
          validators.usernameContent(),
          validators.usernameMinLength(props.options.length_min),
          validators.usernameMaxLength(props.options.length_max),
        ],
      },

      isLoading: false,
    }
  }

  getHelpText() {
    let phrases = []

    if (this.props.options.changes_left > 0) {
      let message = ngettext(
        "You can change your username %(changes_left)s more time.",
        "You can change your username %(changes_left)s more times.",
        this.props.options.changes_left
      )

      phrases.push(
        interpolate(
          message,
          {
            changes_left: this.props.options.changes_left,
          },
          true
        )
      )
    }

    if (this.props.user.acl.name_changes_expire > 0) {
      let message = ngettext(
        "Used changes become available again after %(name_changes_expire)s day.",
        "Used changes become available again after %(name_changes_expire)s days.",
        this.props.user.acl.name_changes_expire
      )

      phrases.push(
        interpolate(
          message,
          {
            name_changes_expire: this.props.user.acl.name_changes_expire,
          },
          true
        )
      )
    }

    return phrases.length ? phrases.join(" ") : null
  }

  clean() {
    let errors = this.validate()
    if (errors.username) {
      snackbar.error(errors.username[0])
      return false
    }
    if (this.state.username.trim() === this.props.user.username) {
      snackbar.info(gettext("Your new username is same as current one."))
      return false
    } else {
      return true
    }
  }

  send() {
    return ajax.post(this.props.user.api.username, {
      username: this.state.username,
    })
  }

  handleSuccess(success) {
    this.setState({
      username: "",
    })

    this.props.complete(success.username, success.slug, success.options)
  }

  handleError(rejection) {
    snackbar.apiError(rejection)
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="panel panel-default panel-form">
          <div className="panel-heading">
            <h3 className="panel-title">{gettext("Change username")}</h3>
          </div>
          <div className="panel-body">
            <FormGroup
              label={gettext("New username")}
              for="id_username"
              helpText={this.getHelpText()}
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
          <div className="panel-footer">
            <Button className="btn-primary" loading={this.state.isLoading}>
              {gettext("Change username")}
            </Button>
          </div>
        </div>
      </form>
    )
  }
}
