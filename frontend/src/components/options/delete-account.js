import React from "react"
import Button from "misago/components/button"
import ajax from "misago/services/ajax"
import title from "misago/services/page-title"
import snackbar from "misago/services/snackbar"
import misago from "misago"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      password: "",
    }
  }

  componentDidMount() {
    title.set({
      title: pgettext("delete your account title", "Delete account"),
      parent: pgettext("forum options", "Change your options"),
    })
  }

  onPasswordChange = (event) => {
    this.setState({ password: event.target.value })
  }

  handleSubmit = (event) => {
    event.preventDefault()

    const { isLoading, password } = this.state
    const { user } = this.props

    if (password.length == 0) {
      snackbar.error(
        pgettext("delete your account form", "Complete the form.")
      )
      return false
    }

    if (isLoading) return false
    this.setState({ isLoading: true })

    ajax.post(user.api.delete, { password }).then(
      (success) => {
        window.location.href = misago.get("MISAGO_PATH")
      },
      (rejection) => {
        this.setState({ isLoading: false })
        if (rejection.password) {
          snackbar.error(rejection.password[0])
        } else {
          snackbar.apiError(rejection)
        }
      }
    )
  }

  render() {
    return (
      <form onSubmit={this.handleSubmit}>
        <div className="panel panel-danger panel-form">
          <div className="panel-heading">
            <h3 className="panel-title">
              {pgettext("delete your account title", "Delete account")}
            </h3>
          </div>
          <div className="panel-body">
            <p>
              {pgettext(
                "delete your account form",
                "This form lets you delete your account. This action is not reversible."
              )}
            </p>
            <p>
              {pgettext(
                "delete your account form",
                "Your account will be deleted together with its profile details, IP addresses and notifications."
              )}
            </p>
            <p>
              {pgettext(
                "delete your account form",
                "Other content will NOT be deleted, but username displayed next to it will be changed to one shared by all deleted accounts."
              )}
            </p>
            <p>
              {pgettext(
                "delete your account form",
                "Your username and e-maill address will become available again for use during registration or for other accounts to change to."
              )}
            </p>
          </div>
          <div className="panel-footer">
            <div className="input-group">
              <input
                className="form-control"
                disabled={this.state.isLoading}
                name="password-confirmation"
                type="password"
                placeholder={pgettext(
                  "delete your account form field",
                  "Enter your password to confirm"
                )}
                value={this.state.password}
                required
                onChange={this.onPasswordChange}
              />
              <span className="input-group-btn">
                <Button className="btn-danger" loading={this.state.isLoading}>
                  {pgettext(
                    "delete your account form btn",
                    "Delete my account"
                  )}
                </Button>
              </span>
            </div>
          </div>
        </div>
      </form>
    )
  }
}
