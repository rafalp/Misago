import React from "react"
import { connect } from "react-redux"
import { patch } from "../../reducers/threads"
import snackbar from "../../services/snackbar"
import { ApiMutation } from "../Api"
import { DropdownSubheader } from "../Dropdown"

const ThreadsListItemNotifications = ({ dispatch, disabled, thread }) => (
  <ApiMutation url={thread.api.watch}>
    {(mutate, { loading }) => {
      function setNotifications(notifications) {
        if (thread.notifications !== notifications) {
          dispatch(patch(thread, { notifications }))
          mutate({
            json: { notifications },
            onError: (error) => {
              snackbar.apiError(error)
              dispatch(patch(thread, { notifications: thread.notifications }))
            },
          })
        }
      }

      return (
        <div className="dropdown">
          <button
            className="btn btn-default btn-icon"
            type="button"
            title={getTitle(thread.notifications)}
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <span className="material-icon">
              {getIcon(thread.notifications)}
            </span>
          </button>
          <ul className="dropdown-menu dropdown-menu-right stick-to-bottom">
            <DropdownSubheader>
              {pgettext("watch thread", "Notify about new replies")}
            </DropdownSubheader>
            <li>
              <button
                className="btn btn-link"
                disabled={disabled || loading}
                onClick={() => setNotifications(2)}
              >
                <span className="material-icon">mail</span>
                {pgettext("watch thread", "Send e-mail notifications")}
              </button>
            </li>
            <li>
              <button
                className="btn btn-link"
                disabled={disabled || loading}
                onClick={() => setNotifications(1)}
              >
                <span className="material-icon">notifications_active</span>
                {pgettext("watch thread", "Without e-mail notifications")}
              </button>
            </li>
            <li>
              <button
                className="btn btn-link"
                disabled={disabled || loading}
                onClick={() => setNotifications(0)}
              >
                <span className="material-icon">notifications_none</span>
                {pgettext("watch thread", "Don't notify")}
              </button>
            </li>
          </ul>
        </div>
      )
    }}
  </ApiMutation>
)

const getIcon = (notifications) => {
  if (notifications === 2) return "mail"
  if (notifications === 1) return "notifications_active"

  return "notifications_none"
}

const getTitle = (notifications) => {
  if (notifications === 2) {
    return pgettext("watch thread", "Send e-mail notifications")
  }

  if (notifications === 1) {
    return pgettext("watch thread", "Without e-mail notifications")
  }

  return gettext("Not watching")
}

const ThreadsListItemNotificationsConnected = connect()(ThreadsListItemNotifications)

export default ThreadsListItemNotificationsConnected
