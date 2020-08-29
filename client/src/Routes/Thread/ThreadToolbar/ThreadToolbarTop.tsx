import React from "react"
import {
  ButtonPrimary,
  Paginator,
  PaginatorCompact,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { ThreadModeration } from "../ThreadModeration"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarTop: React.FC<IThreadToolbarProps> = ({
  moderation,
  pagination,
}) => (
  <>
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
        <ButtonPrimary text="Reply" icon="fas fa-edit" responsive disabled />
      </ToolbarItem>
    </Toolbar>
    {pagination.pages > 1 && (
      <Toolbar portrait>
        <ToolbarItem fill>
          <PaginatorCompact {...pagination} />
        </ToolbarItem>
      </Toolbar>
    )}
  </>
)

export default ThreadToolbarTop
