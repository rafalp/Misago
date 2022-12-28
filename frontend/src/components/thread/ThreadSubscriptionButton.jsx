import classnames from "classnames"
import React from "react"
import * as actions from "../../reducers/thread"
import ajax from "../../services/ajax"
import snackbar from "../../services/snackbar"
import store from "../../services/store"

const ThreadSubscriptionButton = ({ stickToBottom, thread }) => (
  <div className="dropdown">
    <button
      className="btn btn-default btn-outline btn-block"
      aria-expanded="true"
      aria-haspopup="true"
      data-toggle="dropdown"
      type="button"
    >
      <span className="material-icon">{getIcon(thread.subscription)}</span>
      {getLabel(thread.subscription)}
    </button>
    <ul
      className={classnames("dropdown-menu dropdown-menu-right", {
        "stick-to-bottom": stickToBottom,
      })}
    >
      <li>
        <button className="btn btn-link" onClick={() => unsubscribe(thread)}>
          <span className="material-icon">star_border</span>
          {gettext("Unsubscribe")}
        </button>
      </li>
      <li>
        <button className="btn btn-link" onClick={() => alert(thread)}>
          <span className="material-icon">star_half</span>
          {gettext("Subscribe")}
        </button>
      </li>
      <li>
        <button className="btn btn-link" onClick={() => email(thread)}>
          <span className="material-icon">star</span>
          {gettext("Subscribe with e-mail")}
        </button>
      </li>
    </ul>
  </div>
)

function getIcon(subscription) {
  if (subscription === true) return "star"
  if (subscription === false) return "star_half"

  return "star_border"
}

function getLabel(subscription) {
  if (subscription === true) return gettext("E-mail")
  if (subscription === false) return gettext("Enabled")

  return gettext("Disabled")
}

function alert(thread) {
  if (thread.subscription !== false) {
    update(thread, false, "notify")
  }
}

function email(thread) {
  if (thread.subscription !== true) {
    update(thread, true, "email")
  }
}

function unsubscribe(thread) {
  if (thread.subscription !== null) {
    update(thread, null, "unsubscribe")
  }
}

function update(thread, newState, value) {
  const oldState = {
    subscription: thread.subscription,
  }

  store.dispatch(
    actions.update({
      subscription: newState,
    })
  )

  ajax
    .patch(thread.api.index, [
      { op: "replace", path: "subscription", value: value },
    ])
    .then(
      (finalState) => {
        store.dispatch(actions.update(finalState))
      },
      (rejection) => {
        if (rejection.status === 400) {
          snackbar.error(rejection.detail[0])
        } else {
          snackbar.apiError(rejection)
        }

        store.dispatch(actions.update(oldState))
      }
    )
}

export default ThreadSubscriptionButton
