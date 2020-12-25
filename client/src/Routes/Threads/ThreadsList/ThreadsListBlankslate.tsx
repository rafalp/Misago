import { Trans } from "@lingui/macro"
import React from "react"
import { CardBlankslate } from "../../../UI/Card"
import ThreadsNewButton from "../ThreadsNewButton"

interface ThreadsListBlankslateProps {
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsListBlankslate: React.FC<ThreadsListBlankslateProps> = ({
  category,
}) => (
  <CardBlankslate
    header={
      <Trans id="threads.blankslate.header">
        There are no threads in this category.
      </Trans>
    }
    message={
      <Trans id="threads.blankslate.message">
        Why not start one yourself and get the discussion going?
      </Trans>
    }
    actions={<ThreadsNewButton category={category} />}
  />
)

export default ThreadsListBlankslate
