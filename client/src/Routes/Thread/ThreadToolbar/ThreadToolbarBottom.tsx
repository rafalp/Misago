import React from "react"
import { Paginator, Toolbar, ToolbarItem } from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarBottom: React.FC<IThreadToolbarProps> = ({
  page,
  paginatorUrl,
}) => (
  <Toolbar>
    <ToolbarItem>
      <Paginator page={page} url={paginatorUrl} />
    </ToolbarItem>
  </Toolbar>
)

export default ThreadToolbarBottom
