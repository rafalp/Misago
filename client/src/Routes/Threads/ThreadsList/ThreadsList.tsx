import { ApolloError } from "apollo-client"
import React from "react"
import { CardLoader } from "../../../UI/Card"
import { CategoryAcl, Thread } from "../Threads.types"
import ThreadsListBlankslate from "./ThreadsListBlankslate"
import ThreadsListCard from "./ThreadsListCard"
import ThreadsListGraphQLError from "./ThreadsListGraphQLError"
import ThreadsListItem from "./ThreadsListItem/ThreadsListItem"
import ThreadsListUpdateButton from "./ThreadsListUpdateButton"

interface ThreadsListProps {
  acl: CategoryAcl
  category?: {
    id: string
    slug: string
  } | null
  error?: ApolloError | null
  loading?: boolean
  selectable?: boolean
  selection: {
    selection: Record<string, boolean>
    change: (id: string, selected: boolean) => void
  }
  threads: {
    items: Array<Thread>
    nextCursor: string | null
  } | null
  update?: {
    threads: number
    loading: boolean
    fetch: () => void
  } | null
}

const ThreadsList: React.FC<ThreadsListProps> = ({
  acl,
  category,
  error,
  loading,
  selectable,
  selection,
  threads,
  update,
}) => {
  if (loading && !threads) {
    return (
      <ThreadsListCard>
        <CardLoader />
      </ThreadsListCard>
    )
  }

  if (!threads && error) {
    return (
      <ThreadsListCard>
        <ThreadsListGraphQLError error={error} />
      </ThreadsListCard>
    )
  }

  return (
    <ThreadsListCard>
      {update && update.threads > 0 && (
        <ThreadsListUpdateButton
          threads={update.threads}
          loading={update.loading}
          disabled={loading}
          onClick={update.fetch}
        />
      )}
      {threads && threads.items.length > 0 ? (
        <ul className="list-group list-group-flush">
          {threads.items.map((thread) => (
            <ThreadsListItem
              changeSelection={selection.change}
              key={thread.id}
              thread={thread}
              selectable={selectable}
              selected={selection.selection[thread.id]}
            />
          ))}
        </ul>
      ) : (
        <ThreadsListBlankslate acl={acl} category={category} />
      )}
      {loading && <CardLoader />}
    </ThreadsListCard>
  )
}

export default ThreadsList
