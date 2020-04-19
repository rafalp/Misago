import { Trans } from "@lingui/macro"
import React from "react"
import Header from "./Header"

interface IHeaderAllThreadsProps {
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

const HeaderAllThreads: React.FC<IHeaderAllThreadsProps> = ({ settings, stats }) => (
  <Header
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

export default HeaderAllThreads
