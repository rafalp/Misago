import React from "react"
import snackbar from "../../services/snackbar"
import { ApiFetch, ApiMutation } from "../Api"
import PageTitle from "../PageTitle"
import PageContainer from "../PageContainer"
import {
  NotificationsList,
  NotificationsListError,
  NotificationsListLoading,
} from "../NotificationsList"
import NotificationsPills from "./NotificationsPills"
import NotificationsToolbar from "./NotificationsToolbar"

export default function NotificationsRoute({ location, route }) {
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
      <ApiFetch url={getApiUrl(query, filter)}>
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
                        snackbar.success(
                          pgettext("notifications", "All notifications have been marked as read.")
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
      </ApiFetch>
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

function getApiUrl(query, filter) {
  let api = misago.get("NOTIFICATIONS_API") + "?limit=30"
  api += "&filter=" + filter

  if (query.after) {
    api += "&after=" + query.after
  }
  if (query.before) {
    api += "&before=" + query.before
  }

  return api
}
