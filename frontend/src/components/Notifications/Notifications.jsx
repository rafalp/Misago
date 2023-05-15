import React from "react"
import { Router, browserHistory } from "react-router"
import NotificationsHeader from "./NotificationsHeader"
import NotificationsRoute from "./NotificationsRoute"

export default function Notifications() {
  const basename = misago.get("NOTIFICATIONS_URL")

  return (
    <div className="page page-notifications">
      <NotificationsHeader />
      <Router
        history={browserHistory}
        routes={[
          {
            path: basename,
            component: NotificationsRoute,
            props: {
              filter: "all",
            },
          },
          {
            path: basename + "unread/",
            component: NotificationsRoute,
            props: {
              filter: "unread",
            },
          },
          {
            path: basename + "read/",
            component: NotificationsRoute,
            props: {
              filter: "read",
            },
          },
        ]}
      />
    </div>
  )
}
