import React from "react"
import {
  Paginator,
  PaginatorCompact,
  ResetScrollOnNav,
  Responsive,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarBottom: React.FC<IThreadToolbarProps> = ({
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
    </Toolbar>
  </ResetScrollOnNav>
)

export default ThreadToolbarBottom
