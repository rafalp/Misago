import React from "react"
import {
  Paginator,
  ResetScrollOnNav,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarBottom: React.FC<IThreadToolbarProps> = ({
  pagination,
}) => (
  <ResetScrollOnNav selector=".paginator">
    <Toolbar>
      {pagination.pages > 1 && (
        <ToolbarItem>
          <Paginator {...pagination} />
        </ToolbarItem>
      )}
      <ToolbarSeparator />
    </Toolbar>
  </ResetScrollOnNav>
)

export default ThreadToolbarBottom
