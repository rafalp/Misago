import { Trans } from "@lingui/macro"
import React from "react"
import ThreadsHeader from "./ThreadsHeader"

interface IThreadsHeaderAllProps {
  settings: {
    forumIndexHeader: string
    forumIndexThreads: boolean
    forumName: string
  }
  stats: {
    posts: number
    threads: number
    users?: number
  }
}

const ThreadsHeaderAll: React.FC<IThreadsHeaderAllProps> = ({
  settings,
  stats,
}) => (
  <ThreadsHeader
    stats={stats}
    text={
      settings.forumIndexThreads ? (
        settings.forumIndexHeader || settings.forumName
      ) : (
        <Trans id="threads.header">All threads</Trans>
      )
    }
  />
)

export default ThreadsHeaderAll
