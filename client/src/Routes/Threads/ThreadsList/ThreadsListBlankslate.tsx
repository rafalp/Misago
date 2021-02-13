import { Trans } from "@lingui/macro"
import React from "react"
import { CardBlankslate } from "../../../UI/Card"
import { CategoryAcl } from "../Threads.types"
import ThreadsNewButton from "../ThreadsNewButton"

interface ThreadsListBlankslateProps {
  acl: CategoryAcl
  category?: {
    id: string
    slug: string
  } | null
}

const ThreadsListBlankslate: React.FC<ThreadsListBlankslateProps> = ({
  acl,
  category,
}) => (
  <CardBlankslate
    header={
      <Trans id="threads.blankslate.header">
        There are no threads in this category.
      </Trans>
    }
    message={
      acl.start && (
        <Trans id="threads.blankslate.message">
          Why not start one yourself and get the discussion going?
        </Trans>
      )
    }
    actions={acl.start && <ThreadsNewButton category={category} />}
  />
)

export default ThreadsListBlankslate
