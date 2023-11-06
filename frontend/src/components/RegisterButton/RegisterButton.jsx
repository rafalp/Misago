import classnames from "classnames"
import React from "react"
import ajax from "../../services/ajax"
import captcha from "../../services/captcha"
import modal from "../../services/modal"
import snackbar from "../../services/snackbar"
import Loader from "../loader"
import RegisterForm from "../register.js"

export default class RegisterButton extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false,
      isLoaded: false,

      criteria: null,
    }
  }

  showRegisterForm = () => {
    if (this.props.onClick) {
      this.props.onClick()
    }

    if (misago.get("SETTINGS").account_activation === "closed") {
      snackbar.info(
        pgettext(
          "register form",
          "Registration form is currently disabled by the site administrator."
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
              "register form",
              "Registration form is currently unavailable due to an error."
            )
          )
        }
      )
    }
  }

  render() {
    return (
      <button
        className={classnames("btn btn-register", this.props.className, {
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
