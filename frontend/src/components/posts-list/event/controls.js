import React from "react"
import moment from "moment"
import * as post from "misago/reducers/post"
import ajax from "misago/services/ajax"
import snackbar from "misago/services/snackbar"
import store from "misago/services/store"

export default function (props) {
  if (isVisible(props.post.acl)) {
    return (
      <li className="event-controls">
        <Hide {...props} />
        <Unhide {...props} />
        <Delete {...props} />
      </li>
    )
  } else {
    return null
  }
}

export function isVisible(acl) {
  return acl.can_hide
}

export class Hide extends React.Component {
  onClick = () => {
    store.dispatch(
      post.patch(this.props.post, {
        is_hidden: true,
        hidden_on: moment(),
        hidden_by_name: this.props.user.username,
        url: Object.assign(this.props.post.url, {
          hidden_by: this.props.user.url,
        }),
      })
    )

    const op = { op: "replace", path: "is-hidden", value: true }

    ajax.patch(this.props.post.api.index, [op]).then(
      (patch) => {
        store.dispatch(post.patch(this.props.post, patch))
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail[0])
        } else {
          snackbar.apiError(rejection)
        }

        store.dispatch(
          post.patch(this.props.post, {
            is_hidden: false,
          })
        )
      }
    )
  }

  render() {
    if (!this.props.post.is_hidden) {
      return (
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {pgettext("event hide btn", "Hide")}
        </button>
      )
    } else {
      return null
    }
  }
}

export class Unhide extends React.Component {
  onClick = () => {
    store.dispatch(
      post.patch(this.props.post, {
        is_hidden: false,
      })
    )

    const op = { op: "replace", path: "is-hidden", value: false }

    ajax.patch(this.props.post.api.index, [op]).then(
      (patch) => {
        store.dispatch(post.patch(this.props.post, patch))
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail[0])
        } else {
          snackbar.apiError(rejection)
        }

        store.dispatch(
          post.patch(this.props.post, {
            is_hidden: true,
          })
        )
      }
    )
  }

  render() {
    if (this.props.post.is_hidden) {
      return (
        <button type="button" className="btn btn-link" onClick={this.onClick}>
          {pgettext("event reveal btn", "Unhide")}
        </button>
      )
    } else {
      return null
    }
  }
}

export class Delete extends React.Component {
  onClick = () => {
    const decision = window.confirm(
      pgettext(
        "event delete",
        "Are you sure you wish to delete this event? This action is not reversible!"
      )
    )
    if (decision) {
      this.delete()
    }
  }

  delete = () => {
    store.dispatch(
      post.patch(this.props.post, {
        isDeleted: true,
      })
    )

    ajax.delete(this.props.post.api.index).then(
      () => {
        snackbar.success(pgettext("event delete", "Event has been deleted."))
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail[0])
        } else {
          snackbar.apiError(rejection)
        }

        store.dispatch(
          post.patch(this.props.post, {
            isDeleted: false,
          })
        )
      }
    )
  }

  render() {
    return (
      <button type="button" className="btn btn-link" onClick={this.onClick}>
        {pgettext("event delete btn", "Delete")}
      </button>
    )
  }
}
