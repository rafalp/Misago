import React from "react"
import Button from "misago/components/button"
import { patch } from "misago/reducers/threads"
import ajax from "misago/services/ajax"
import modal from "misago/services/modal"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

const STATE_UPDATES = {
  unsubscribe: null,
  notify: false,
  email: true
}

export default class extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      isLoading: false
    }
  }

  setSubscription = newState => {
    modal.hide()

    this.setState({
      isLoading: true
    })

    let oldState = this.props.thread.subscription

    store.dispatch(
      patch(this.props.thread, {
        subscription: STATE_UPDATES[newState]
      })
    )

    ajax
      .patch(this.props.thread.api.index, [
        { op: "replace", path: "subscription", value: newState }
      ])
      .then(
        () => {
          this.setState({
            isLoading: false
          })
        },
        rejection => {
          this.setState({
            isLoading: false
          })
          store.dispatch(
            patch(this.props.thread, {
              subscription: STATE_UPDATES[oldState]
            })
          )
          snackbar.apiError(rejection)
        }
      )
  }

  unsubscribe = () => {
    this.setSubscription("unsubscribe")
  }

  notify = () => {
    this.setSubscription("notify")
  }

  email = () => {
    this.setSubscription("email")
  }

  render() {
    return (
      <ul className={this.props.className}>
        <li>
          <button className="btn-link" onClick={this.unsubscribe}>
            <span className="material-icon">star_border</span>
            {gettext("Unsubscribe")}
          </button>
        </li>
        <li>
          <button className="btn-link" onClick={this.notify}>
            <span className="material-icon">star_half</span>
            {gettext("Subscribe")}
          </button>
        </li>
        <li>
          <button className="btn-link" onClick={this.email}>
            <span className="material-icon">star</span>
            {gettext("Subscribe with e-mail")}
          </button>
        </li>
      </ul>
    )
  }
}
