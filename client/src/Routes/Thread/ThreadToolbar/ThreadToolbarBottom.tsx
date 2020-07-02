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
  <ResetScrollOnNav selector=".paginator">
    {pagination.pages > 1 && (
      <Toolbar portrait>
        <ToolbarItem fill>
          <PaginatorCompact {...pagination} />
        </ToolbarItem>
      </Toolbar>
    )}
    <Toolbar>
      {pagination.pages > 1 && (
        <ToolbarItem>
          <Responsive landscape tablet>
            <PaginatorCompact {...pagination} />
          </Responsive>
          <Responsive desktop>
            <Paginator {...pagination} />
          </Responsive>
        </ToolbarItem>
      )}
      <ToolbarSeparator />
    </Toolbar>
  </ResetScrollOnNav>
)

export default ThreadToolbarBottom
