import classnames from "classnames"
import React from "react"
import { connect } from "react-redux"
import { update } from "../../reducers/thread"
import snackbar from "../../services/snackbar"
import { ApiMutation } from "../Api"
import { DropdownSubheader } from "../Dropdown"

const ThreadWatchButton = ({ dispatch, dropup, stickToBottom, thread }) => (
  <ApiMutation url={thread.api.watch}>
    {(mutate, { loading }) => {
      function setNotifications(notifications) {
        if (thread.notifications !== notifications) {
          dispatch(update({ notifications }))
          mutate({
            json: { notifications },
            onError: (error) => {
              snackbar.apiError(error)
              dispatch(update({ notifications: thread.notifications }))
            },
          })
        }
      }

      return (
        <div className={dropup ? "dropup" : "dropdown"}>
          <button
            className="btn btn-default btn-outline btn-block"
            aria-expanded="true"
            aria-haspopup="true"
            data-toggle="dropdown"
            type="button"
          >
            <span className="material-icon">
              {getIcon(thread.notifications)}
            </span>
            {getLabel(thread.notifications)}
          </button>
          <ul
            className={classnames("dropdown-menu dropdown-menu-right", {
              "stick-to-bottom": stickToBottom,
            })}
          >
            <DropdownSubheader>
              {pgettext("watch thread", "Notify about new replies")}
            </DropdownSubheader>
            <li>
              <button
                className="btn btn-link"
                disabled={loading}
                onClick={() => setNotifications(2)}
              >
                <span className="material-icon">mail</span>
                {pgettext("watch thread", "On site and with e-mail")}
              </button>
            </li>
            <li>
              <button
                className="btn btn-link"
                disabled={loading}
                onClick={() => setNotifications(1)}
              >
                <span className="material-icon">notifications_active</span>
                {pgettext("watch thread", "On site only")}
              </button>
            </li>
            <li>
              <button
                className="btn btn-link"
                disabled={loading}
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

function getIcon(notifications) {
  if (notifications === 2) return "mail"
  if (notifications === 1) return "notifications_active"

  return "notifications_none"
}

function getLabel(notifications) {
  if (notifications) {
    return pgettext("watch thread", "Watching")
  }

  return pgettext("watch thread", "Watch")
}

const ThreadWatchButtonConnected = connect()(ThreadWatchButton)

export default ThreadWatchButtonConnected
