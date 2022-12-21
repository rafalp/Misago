import React from "react"
import { patch } from "../../reducers/threads"
import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"
import store from "../../services/store"

const SUBSCRIPTION = {
  unsubscribe: null,
  notify: false,
  email: true
}

class ThreadsListItemSubscriptionOptions extends React.Component { 
  constructor(props) {
    super(props)

    this.state = {
      loading: false
    }
  }

  update = (value) => {
    const { thread } = this.props

    this.setState({loading: true})
    store.dispatch(
      patch(thread, { subscription: SUBSCRIPTION[value] })
    )

    ajax
      .patch(thread.api.index, [
        { op: "replace", path: "subscription", value }
      ])
      .then(
        () => {},
        rejection => {
          store.dispatch(
            patch(thread, {
              subscription: SUBSCRIPTION[thread.subscription]
            })
          )
          snackbar.apiError(rejection)
        }
      ).then(() => this.setState({loading: false}))
  }

  render = () => {
    const { loading } = this.state
    const { disabled, thread } = this.props

    return (
      <ul className="dropdown-menu dropdown-menu-right">
        <li>
          <button
            className="btn-link"
            disabled={disabled || loading || thread.subscription === null}
            onClick={() => this.update("unsubscribe")}
          >
            <span className="material-icon">star_border</span>
            {gettext("Unsubscribe")}
          </button>
        </li>
        <li>
          <button
            className="btn-link"
            disabled={disabled || loading || thread.subscription === false}
            onClick={() => this.update("notify")}
          >
            <span className="material-icon">star_half</span>
            {gettext("Subscribe with alert")}
          </button>
        </li>
        <li>
          <button
            className="btn-link"
            disabled={disabled || loading || thread.subscription === true}
            onClick={() => this.update("email")}
          >
            <span className="material-icon">star</span>
            {gettext("Subscribe with e-mail")}
          </button>
        </li>
      </ul>
    )
  }
}

export default ThreadsListItemSubscriptionOptions
