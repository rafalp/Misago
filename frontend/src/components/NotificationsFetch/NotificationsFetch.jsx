import React from "react"
import { connect } from "react-redux"
import { updateAuthenticatedUser } from "../../reducers/auth"
import { ApiFetch } from "../Api"

function NotificationsFetch({
  children,
  filter,
  query,
  dispatch,
  unreadNotifications,
  disabled,
}) {
  return (
    <ApiFetch
      url={getApiUrl(filter, query)}
      disabled={disabled}
      onData={(data) => {
        if (data.unreadNotifications != unreadNotifications) {
          dispatch(
            updateAuthenticatedUser({
              unreadNotifications: data.unreadNotifications,
            })
          )
        }
      }}
    >
      {({ data, loading, error, refetch }) => {
        return children({ data, loading, error, refetch })
      }}
    </ApiFetch>
  )
}

function getApiUrl(filter, query) {
  let api = misago.get("NOTIFICATIONS_API") + "?limit=30"
  api += "&filter=" + filter

  if (query) {
    if (query.after) {
      api += "&after=" + query.after
    }
    if (query.before) {
      api += "&before=" + query.before
    }
  }

  return api
}

function selectState({ auth }) {
  if (!auth.user) {
    return { unreadNotifications: null }
  }

  return {
    unreadNotifications: auth.user.unreadNotifications,
  }
}

const NotificationsFetchConnected = connect(selectState)(NotificationsFetch)

export default NotificationsFetchConnected
