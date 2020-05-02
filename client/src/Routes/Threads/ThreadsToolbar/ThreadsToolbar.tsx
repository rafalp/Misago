import React from "react"
import { Toolbar, ToolbarItem, ToolbarSeparator } from "../../../UI"
import ThreadsStartButton from "../ThreadsStartButton"

interface IThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<IThreadsToolbarProps> = ({ category }) => (
  <>
    <Toolbar mobile>
      <ToolbarSeparator />
      <ToolbarItem>
        <ThreadsStartButton category={category} small />
      </ToolbarItem>
    </Toolbar>
    <Toolbar desktop>
      <ToolbarSeparator />
      <ToolbarItem>
        <ThreadsStartButton category={category} />
      </ToolbarItem>
    </Toolbar>
  </>
)

export default ThreadsToolbar
