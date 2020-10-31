import React from "react"
import { Paginator, PaginatorCompact } from "../../../UI/Paginator"
import ResetScrollOnNav from "../../../UI/ResetScrollOnNav"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import { ThreadModeration } from "../ThreadModeration"
import { IThreadToolbarProps } from "./ThreadToolbar.types"
import ThreadToolbarReplyButton from "./ThreadToolbarReplyButton"

const ThreadToolbarBottom: React.FC<IThreadToolbarProps> = ({
  isClosed,
  moderation,
  pagination,
}) => (
  <ResetScrollOnNav selector=".toolbar">
    {pagination.pages > 1 && (
      <Toolbar portrait>
        <ToolbarItem fill>
          <PaginatorCompact {...pagination} />
        </ToolbarItem>
      </Toolbar>
    )}
    <Toolbar>
      {pagination.pages > 1 && (
        <>
          <ToolbarItem landscape tablet>
            <PaginatorCompact {...pagination} />
          </ToolbarItem>
          <ToolbarItem desktop>
            <Paginator {...pagination} />
          </ToolbarItem>
        </>
      )}
      <ToolbarSeparator />
      {moderation && (
        <ToolbarItem>
          <ThreadModeration moderation={moderation} />
        </ToolbarItem>
      )}
      <ToolbarItem>
        <ThreadToolbarReplyButton isClosed={isClosed} />
      </ToolbarItem>
    </Toolbar>
  </ResetScrollOnNav>
)

export default ThreadToolbarBottom
