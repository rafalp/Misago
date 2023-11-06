/* global grecaptcha */
import React from "react"
import FormGroup from "misago/components/form-group"

export class BaseCaptcha {
  init(context, ajax, include, snackbar) {
    this._context = context
    this._ajax = ajax
    this._include = include
    this._snackbar = snackbar
  }
}

export class NoCaptcha extends BaseCaptcha {
  load() {
    return new Promise(function (resolve) {
      // immediately resolve as we don't have anything to validate
      resolve()
    })
  }

  validator() {
    return null
  }

  component() {
    return null
  }
}

export class QACaptcha extends BaseCaptcha {
  load() {
    var self = this
    return new Promise((resolve, reject) => {
      self._ajax.get(self._context.get("CAPTCHA_API")).then(
        function (data) {
          self.question = data.question
          self.helpText = data.help_text
          resolve()
        },
        function () {
          self._snackbar.error(
            pgettext("captcha field", "Failed to load CAPTCHA.")
          )
          reject()
        }
      )
    })
  }

  validator() {
    return []
  }

  component(kwargs) {
    return (
      <FormGroup
        label={this.question}
        for="id_captcha"
        labelClass={kwargs.labelClass || ""}
        controlClass={kwargs.controlClass || ""}
        validation={kwargs.form.state.errors.captcha}
        helpText={this.helpText || null}
      >
        <input
          aria-describedby="id_captcha_status"
          className="form-control"
          disabled={kwargs.form.state.isLoading}
          id="id_captcha"
          onChange={kwargs.form.bindInput("captcha")}
          type="text"
          value={kwargs.form.state.captcha}
        />
      </FormGroup>
    )
  }
}

export class ReCaptchaComponent extends React.Component {
  componentDidMount() {
    grecaptcha.render("recaptcha", {
      sitekey: this.props.siteKey,
      callback: (response) => {
        // fire fakey event to binding
        this.props.binding({
          target: {
            value: response,
          },
        })
      },
    })
  }

  render() {
    return <div id="recaptcha" />
  }
}

export class ReCaptcha extends BaseCaptcha {
  load() {
    this._include.include("https://www.google.com/recaptcha/api.js", true)

    return new Promise(function (resolve) {
      var wait = function () {
        if (typeof grecaptcha === "undefined") {
          window.setTimeout(function () {
            wait()
          }, 200)
        } else {
          resolve()
        }
      }
      wait()
    })
  }

  validator() {
    return []
  }

  component(kwargs) {
    return (
      <FormGroup
        label={pgettext("captcha field", "Please solve the quick test")}
        for="id_captcha"
        labelClass={kwargs.labelClass || ""}
        controlClass={kwargs.controlClass || ""}
        validation={kwargs.form.state.errors.captcha}
        helpText={pgettext(
          "captcha field",
          "This test helps us prevent automated spam registrations on the site."
        )}
      >
        <ReCaptchaComponent
          binding={kwargs.form.bindInput("captcha")}
          siteKey={this._context.get("SETTINGS").recaptcha_site_key}
        />
      </FormGroup>
    )
  }
}

export class Captcha {
  init(context, ajax, include, snackbar) {
    switch (context.get("SETTINGS").captcha_type) {
      case "no":
        this._captcha = new NoCaptcha()
        break

      case "qa":
        this._captcha = new QACaptcha()
        break

      case "re":
        this._captcha = new ReCaptcha()
        break
    }

    this._captcha.init(context, ajax, include, snackbar)
  }

  // accessors for underlying strategy

  load() {
    return this._captcha.load()
  }

  validator() {
    return this._captcha.validator()
  }

  component(kwargs) {
    return this._captcha.component(kwargs)
  }
}

export default new Captcha()
