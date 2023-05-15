import React from "react"
import { connect } from "react-redux"
import { updateAuthenticatedUser } from "../../reducers/auth"
import snackbar from "../../services/snackbar"
import { ApiMutation } from "../Api"
import NotificationsFetch from "../NotificationsFetch"
import PageTitle from "../PageTitle"
import PageContainer from "../PageContainer"
import {
  NotificationsList,
  NotificationsListError,
  NotificationsListLoading,
} from "../NotificationsList"
import NotificationsPills from "./NotificationsPills"
import NotificationsToolbar from "./NotificationsToolbar"

function NotificationsRoute({ dispatch, location, route }) {
  const { query } = location
  const { filter } = route.props

  const baseUrl = getBaseUrl(filter)

  return (
    <PageContainer>
      <PageTitle
        title={pgettext("notifications title", "Notifications")}
        subtitle={getSubtitle(filter)}
      />

      <NotificationsPills filter={filter} />

      <NotificationsFetch filter={filter} query={query}>
        {({ data, loading, error, refetch }) => (
          <ApiMutation url={misago.get("NOTIFICATIONS_API") + "read-all/"}>
            {(readAll, { loading: mutating }) => {
              const toolbarProps = {
                baseUrl,
                data,
                disabled:
                  loading || mutating || !data || data.results.length === 0,
                markAllAsRead: async () => {
                  const confirmed = window.confirm(
                    pgettext("notifications", "Mark all notifications as read?")
                  )

                  if (confirmed) {
                    readAll({
                      onSuccess: async () => {
                        refetch()
                        dispatch(
                          updateAuthenticatedUser({ unreadNotifications: null })
                        )
                        snackbar.success(
                          pgettext(
                            "notifications",
                            "All notifications have been marked as read."
                          )
                        )
                      },
                      onError: snackbar.apiError,
                    })
                  }
                },
              }

              if (loading || mutating) {
                return (
                  <div>
                    <NotificationsToolbar {...toolbarProps} />
                    <NotificationsListLoading />
                    <NotificationsToolbar {...toolbarProps} bottom />
                  </div>
                )
              }

              if (error) {
                return (
                  <div>
                    <NotificationsToolbar {...toolbarProps} />
                    <NotificationsListError error={error} />
                    <NotificationsToolbar {...toolbarProps} bottom />
                  </div>
                )
              }

              if (data) {
                if (!data.hasPrevious && query) {
                  window.history.replaceState({}, "", baseUrl)
                }

                return (
                  <div>
                    <NotificationsToolbar {...toolbarProps} />
                    <NotificationsList
                      filter={filter}
                      items={data.results}
                      hasNext={data.hasNext}
                      hasPrevious={data.hasPrevious}
                    />
                    <NotificationsToolbar {...toolbarProps} bottom />
                  </div>
                )
              }

              return null
            }}
          </ApiMutation>
        )}
      </NotificationsFetch>
    </PageContainer>
  )
}

function getSubtitle(filter) {
  if (filter === "unread") {
    return pgettext("notifications title", "Unread notifications")
  } else if (filter === "read") {
    return pgettext("notifications title", "Read notifications")
  } else {
    return null
  }
}

function getBaseUrl(filter) {
  let url = misago.get("NOTIFICATIONS_URL")
  if (filter !== "all") {
    url += filter + "/"
  }
  return url
}

const NotificationsRouteConnected = connect()(NotificationsRoute)

export default NotificationsRouteConnected
