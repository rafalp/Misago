import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection } from "../../Toolbar"
import RankUsersLeft from "./RankUsersLeft"
import RankUsersPagination from "./RankUsersPagination"

const RankUsersToolbar = ({ baseUrl, users }) => (
  <Toolbar>
    <ToolbarSection>
      <ToolbarItem>
        <RankUsersPagination baseUrl={baseUrl} users={users} />
      </ToolbarItem>
    </ToolbarSection>
    <ToolbarSection auto>
      <ToolbarItem>
        <RankUsersLeft users={users} />
      </ToolbarItem>
    </ToolbarSection>
  </Toolbar>
)

export default RankUsersToolbar
