import React from "react"
import zxcvbn from "misago/services/zxcvbn"

export const STYLES = [
  "progress-bar-danger",
  "progress-bar-warning",
  "progress-bar-warning",
  "progress-bar-primary",
  "progress-bar-success",
]

export const LABELS = [
  pgettext("password strength indicator", "Entered password is very weak."),
  pgettext("password strength indicator", "Entered password is weak."),
  pgettext("password strength indicator", "Entered password is average."),
  pgettext("password strength indicator", "Entered password is strong."),
  pgettext("password strength indicator", "Entered password is very strong."),
]

export default class extends React.Component {
  constructor(props) {
    super(props)

    this._score = 0
    this._password = null
    this._inputs = []

    this.state = {
      loaded: false,
    }
  }

  componentDidMount() {
    zxcvbn.load().then(() => {
      this.setState({ loaded: true })
    })
  }

  getScore(password, inputs) {
    let cacheStale = false

    if (password !== this._password) {
      cacheStale = true
    }

    if (inputs.length !== this._inputs.length) {
      cacheStale = true
    } else {
      inputs.map((value, i) => {
        if (value.trim() !== this._inputs[i]) {
          cacheStale = true
        }
      })
    }

    if (cacheStale) {
      this._score = zxcvbn.scorePassword(password, inputs)
      this._password = password
      this._inputs = inputs.map(function (value) {
        return value.trim()
      })
    }

    return this._score
  }

  render() {
    if (!this.state.loaded) return null

    let score = this.getScore(this.props.password, this.props.inputs)

    return (
      <div className="help-block password-strength">
        <div className="progress">
          <div
            className={"progress-bar " + STYLES[score]}
            style={{ width: 20 + 20 * score + "%" }}
            role="progress-bar"
            aria-valuenow={score}
            aria-valuemin="0"
            aria-valuemax="4"
          >
            <span className="sr-only">{LABELS[score]}</span>
          </div>
        </div>
        <p className="text-small">{LABELS[score]}</p>
      </div>
    )
  }
}
