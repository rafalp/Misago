import { Trans } from "@lingui/macro"
import React from "react"
import Header from "./Header"

interface IHeaderAllThreadsProps {
  settings: {
    forumIndexHeader: string
    forumIndexThreads: boolean
    forumName: string
  }
}

const HeaderAllThreads: React.FC<IHeaderAllThreadsProps> = ({ settings }) => (
  <Header
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
