import React from "react"
import {
  ButtonPrimary,
  Paginator,
  PaginatorCompact,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarTop: React.FC<IThreadToolbarProps> = ({ pagination }) => (
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
      <ToolbarItem>
        <ButtonPrimary
          text="Reply"
          icon="edit"
          iconSolid
          responsive
          disabled
        />
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
