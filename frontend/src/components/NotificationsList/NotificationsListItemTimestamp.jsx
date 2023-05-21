import React from "react"
import Timestamp from "../Timestamp"

export default function NotificationsListItemTimestamp({ notification }) {
  return (
    <div className="notifications-list-item-timestamp">
      <Timestamp datetime={notification.createdAt} />
    </div>
  )
}
