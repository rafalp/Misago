import { Trans } from "@lingui/macro"
import React from "react"
import Header from "./Header"

interface IAllThreadsHeaderProps {
  settings: {
    forumIndexHeader: string
    forumIndexThreads: boolean
    forumName: string
  }
}

const AllThreadsHeader: React.FC<IAllThreadsHeaderProps> = ({ settings }) => (
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

export default AllThreadsHeader
