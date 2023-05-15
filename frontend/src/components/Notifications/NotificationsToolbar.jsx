import classnames from "classnames"
import React from "react"
import Button from "../button"
import { Toolbar, ToolbarSection, ToolbarItem, ToolbarSpacer } from "../Toolbar"
import NotificationsPagination from "./NotificationsPagination"

export default function NotificationsToolbar({
  baseUrl,
  data,
  disabled,
  bottom,
  markAllAsRead,
}) {
  return (
    <Toolbar>
      <ToolbarSection>
        <ToolbarItem>
          <NotificationsPagination
            baseUrl={baseUrl}
            data={data}
            disabled={disabled}
          />
        </ToolbarItem>
      </ToolbarSection>
      <ToolbarSpacer />
      <ToolbarSection className={classnames({ "hidden-xs": !bottom })}>
        <ToolbarItem>
          <Button
            className="btn-default btn-block"
            type="button"
            disabled={disabled || !data || !data.unreadNotifications}
            onClick={markAllAsRead}
          >
            <span className="material-icon">done_all</span>
            {pgettext("notifications", "Mark all as read")}
          </Button>
        </ToolbarItem>
      </ToolbarSection>
    </Toolbar>
  )
}
