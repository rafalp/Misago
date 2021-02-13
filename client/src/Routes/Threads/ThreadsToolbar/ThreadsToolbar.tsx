import React from "react"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import { CategoryAcl } from "../Threads.types"
import ThreadsNewButton from "../ThreadsNewButton"

interface ThreadsToolbarProps {
  acl: CategoryAcl
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<ThreadsToolbarProps> = ({ acl, category }) => (
  <Toolbar>
    <ToolbarSeparator />
    {acl.start && (
      <ToolbarItem>
        <ThreadsNewButton category={category} />
      </ToolbarItem>
    )}
  </Toolbar>
)

export default ThreadsToolbar
