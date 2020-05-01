import React from "react"
import ThreadsStartButton from "../ThreadsStartButton"

interface IThreadsToolbarProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsToolbar: React.FC<IThreadsToolbarProps> = ({ category }) => (
  <div className="row">
    <div className="col">
      <ThreadsStartButton category={category} />
    </div>
  </div>
)

export default ThreadsToolbar
