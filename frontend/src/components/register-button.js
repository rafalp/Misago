import classnames from "classnames"
import React from "react"
import Loader from "misago/components/loader"
import RegisterForm from "misago/components/register.js"
import ajax from "misago/services/ajax"
import captcha from "misago/services/captcha"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      isLoaded: false,

      criteria: null,
    }
  }

  showRegisterForm = () => {
    if (misago.get("SETTINGS").account_activation === "closed") {
      snackbar.info(
        pgettext(
          "registration btn error",
          "New registrations are currently disabled."
        )
      )
    } else if (this.state.isLoaded) {
      modal.show(<RegisterForm criteria={this.state.criteria} />)
    } else {
      this.setState({ isLoading: true })

      Promise.all([
        captcha.load(),
        ajax.get(misago.get("AUTH_CRITERIA_API")),
      ]).then(
        (result) => {
          this.setState({
            isLoading: false,
            isLoaded: true,
            criteria: result[1],
          })

          modal.show(<RegisterForm criteria={result[1]} />)
        },
        () => {
          this.setState({ isLoading: false })

          snackbar.error(
            pgettext(
              "registration btn error",
              "Registration is currently unavailable due to an error."
            )
          )
        }
      )
    }
  }

  render() {
    return (
      <button
        className={classnames("btn btn-register", {
          "btn-block": this.props.block,
          "btn-loading": this.state.isLoading,
        })}
        disabled={this.state.isLoading}
        onClick={this.showRegisterForm}
        type="button"
      >
        {pgettext("cta", "Register")}
        {this.state.isLoading ? <Loader /> : null}
      </button>
    )
  }
}
