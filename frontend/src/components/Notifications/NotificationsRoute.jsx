import React from "react"
import { ApiFetch } from "../Api"
import PageTitle from "../PageTitle"
import PageContainer from "../PageContainer"
import NotificationsList from "./NotificationsList"
import NotificationsListEmpty from "./NotificationsListEmpty"
import NotificationsLoading from "./NotificationsLoading"
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
        {({ data, loading, error, refetch }) => {
          const toolbarProps = {
            baseUrl,
            data,
            refetch,
            disabled: loading || !data || data.results.length === 0,
          }

          if (loading) {
            return (
              <div>
                <NotificationsToolbar {...toolbarProps} />
                <NotificationsLoading />
                <NotificationsToolbar {...toolbarProps} bottom />
              </div>
            )
          }

          if (error) {
            return <div>{JSON.stringify(error)}</div>
          }

          if (data) {
            if (!data.hasPrevious && query) {
              window.history.replaceState({}, "", baseUrl)
            }

            return (
              <div>
                <NotificationsToolbar {...toolbarProps} />
                {data.results.length > 0 ? (
                  <NotificationsList
                    items={data.results}
                    hasNext={data.hasNext}
                    hasPrevious={data.hasPrevious}
                  />
                ) : (
                  <NotificationsListEmpty filter={filter} />
                )}
                <NotificationsToolbar {...toolbarProps} bottom />
              </div>
            )
          }

          return null
        }}
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
