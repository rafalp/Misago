import React from "react"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI/Toolbar"
import ThreadsNewButton from "../ThreadsNewButton"

interface ThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<ThreadsToolbarProps> = ({ category }) => (
  <Toolbar>
    <ToolbarSeparator />
    <ToolbarItem>
      <ThreadsNewButton category={category} />
    </ToolbarItem>
  </Toolbar>
)

export default ThreadsToolbar
