import React from "react"
import { ApiFetch } from "../Api"
import PageTitle from "../PageTitle"
import PageContainer from "../PageContainer"
import NotificationsList from "./NotificationsList"
import NotificationsNav from "./NotificationsNav"

export default function NotificationsRoute({ location, route }) {
  const { query } = location
  const { filter } = route.props

  return (
    <PageContainer>
      <PageTitle
        title={pgettext("notifications title", "Notifications")}
        subtitle={getSubtitle(filter)}
      />

      <NotificationsNav filter={filter} />

      <ApiFetch url={getApiUrl(query, filter)}>
        {({ data, loading, error }) => {
          if (loading) {
            return <div>LOADING</div>
          }

          if (data) {
            return (
              <NotificationsList
                items={data.results}
                hasNext={data.hasNext}
                hasPrevious={data.hasPrevious}
              />
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

function getApiUrl(query, filter) {
  let api = misago.get("NOTIFICATIONS_API") + "?limit=50"
  api += "&filter=" + filter
  return api
}
