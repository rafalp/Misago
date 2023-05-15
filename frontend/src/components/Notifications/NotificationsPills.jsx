import React from "react"
import { PillsNav, PillsNavLink } from "../PillsNav"
import { Toolbar, ToolbarSection, ToolbarItem } from "../Toolbar"

export default function NotificationsPills({ filter }) {
  const basename = misago.get("NOTIFICATIONS_URL")

  return (
    <Toolbar>
      <ToolbarSection auto>
        <ToolbarItem>
          <PillsNav>
            <PillsNavLink active={filter === "all"} link={basename}>
              {pgettext("notifications nav", "All")}
            </PillsNavLink>
            <PillsNavLink
              active={filter === "unread"}
              link={basename + "unread/"}
            >
              {pgettext("notifications nav", "Unread")}
            </PillsNavLink>
            <PillsNavLink active={filter === "read"} link={basename + "read/"}>
              {pgettext("notifications nav", "Read")}
            </PillsNavLink>
          </PillsNav>
        </ToolbarItem>
      </ToolbarSection>
    </Toolbar>
  )
}
