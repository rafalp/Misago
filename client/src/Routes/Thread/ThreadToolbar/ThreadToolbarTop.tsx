import React from "react"
import {
  Paginator,
  ButtonPrimary,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarTop: React.FC<IThreadToolbarProps> = ({ pagination }) => (
  <Toolbar>
    {pagination.pages > 1 && (
      <ToolbarItem>
        <Paginator {...pagination} />
      </ToolbarItem>
    )}
    <ToolbarSeparator />
    <ToolbarItem>
      <ButtonPrimary text="Reply" icon="edit" iconSolid responsive disabled />
    </ToolbarItem>
  </Toolbar>
)

export default ThreadToolbarTop
