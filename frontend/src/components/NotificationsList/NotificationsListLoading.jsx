import React from "react"
import { ListGroupLoading } from "../ListGroup"
import NotificationsListGroup from "./NotificationsListGroup"

export default function NotificationsListLoading() {
  return (
    <NotificationsListGroup className="notifications-list-pending">
      <ListGroupLoading
        message={pgettext("notifications list", "Loading notifications...")}
      />
    </NotificationsListGroup>
  )
}
