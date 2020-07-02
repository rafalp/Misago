import React from "react"
import {
  ButtonPrimary,
  Paginator,
  PaginatorCompact,
  Responsive,
  Toolbar,
  ToolbarItem,
  ToolbarSeparator,
} from "../../../UI"
import { IThreadToolbarProps } from "./ThreadToolbar.types"

const ThreadToolbarTop: React.FC<IThreadToolbarProps> = ({ pagination }) => (
  <>
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
