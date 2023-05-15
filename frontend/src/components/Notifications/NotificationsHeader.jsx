import React from "react"
import { PageHeaderPlain } from "../PageHeader"

export default function NotificationsHeader() {
  return (
    <PageHeaderPlain
      header={pgettext("notifications title", "Notifications")}
      styleName="notifications"
    />
  )
}
