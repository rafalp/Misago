import React from "react"
import { patch } from "misago/reducers/threads"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default function(props) {
  if (!props.user.id) return null

  return (
    <div className={props.className}>
      <button
        aria-expanded="true"
        aria-haspopup="true"
        className="btn btn-default dropdown-toggle btn-block btn-outline"
        data-toggle="dropdown"
        type="button"
      >
        <span className="material-icon">subscriptions</span>
        <span className="hidden-xs">{gettext("Subscriptions")}</span>
      </button>
      <Dropdown {...props} />
    </div>
  )
}

export function Dropdown(props) {
  return (
    <ul className={props.dropdownClassName || "dropdown-menu stick-to-bottom"}>
      <Disable {...props} />
      <Enable {...props} />
      <Email {...props} />
    </ul>
  )
}

export class Disable extends React.Component {
  onClick = () => {
    if (this.props.threads === null || this.props.threads.length === 0) {
      return
    }

    update(this.props.threads, null, "unsubscribe")
  }

  render() {
    return (
      <li>
        <button className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">star_border</span>
          {gettext("Unsubscribe All")}
        </button>
      </li>
    )
  }
}

export class Enable extends React.Component {
  onClick = () => {
    if (this.props.threads === null || this.props.threads.length === 0) {
      return
    }

    update(this.props.threads, false, "notify")
  }

  render() {
    return (
      <li>
        <button className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">star_half</span>
          {gettext("Subscribe All")}
        </button>
      </li>
    )
  }
}

export class Email extends React.Component {
  onClick = () => {
    if (this.props.threads === null || this.props.threads.length === 0) {
      return
    }

    update(this.props.threads, true, "email")
  }

  render() {
    return (
      <li>
        <button className="btn btn-link" onClick={this.onClick}>
          <span className="material-icon">star</span>
          {gettext("Subscribe E-mail All")}
        </button>
      </li>
    )
  }
}

export function update(threads, newState, value) {
  const oldThreads = threads

  threads.map(thread => {
    store.dispatch(
      patch(thread, {
        subscription: newState
      })
    )
  })

  // TODO pull this from threads?
  ajax
    .patch("/api/threads/" /*thread.api.index*/, {
      ids: threads.map(t => t.id),
      ops: [
        {
          op: "replace",
          path: "subscription",
          value: value
        }
      ]
    })

    .then(
      // this feels redundant, but it's also what's being done in single thread.
      finalState => {
        finalState.map(thread => {
          store.dispatch(
            patch(thread, {
              subscription: thread.subscription
            })
          )
        })
      },
      rejection => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail[0])
        } else {
          snackbar.apiError(rejection)
        }

        oldThreads.map(thread => {
          store.dispatch(
            patch(thread, {
              subscription: thread.subscription
            })
          )
        })
      }
    )
}
