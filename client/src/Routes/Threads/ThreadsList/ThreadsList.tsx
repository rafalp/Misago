import { ApolloError } from "apollo-client"
import React from "react"
import { Link } from "react-router-dom"
import { CardLoader } from "../../../UI"
import * as urls from "../../../urls"
import { IThread } from "../Threads.types"
import ThreadsListCard from "./ThreadsListCard"
import ThreadsListBlankslate from "./ThreadsListBlankslate"
import ThreadsListGraphQLError from "./ThreadsListGraphQLError"
import ThreadsListUpdateButton from "./ThreadsListUpdateButton"

interface IThreadsListProps {
  category?: {
    id: string
    slug: string
  } | null
  loading?: boolean
  error?: ApolloError | null
  threads: {
    items: Array<IThread>
    nextCursor: string | null
  } | null
  update?: {
    threads: number
    loading: boolean
    fetch: () => void
  } | null
}

const ThreadsList: React.FC<IThreadsListProps> = ({
  category,
  error,
  loading,
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
            <li className="list-group-item" key={thread.id}>
              <strong>
                <Link to={urls.thread(thread)}>{thread.title}</Link>
              </strong>
              <ul className="list-inline">
                {thread.category.parent && (
                  <li className="list-inline-item">
                    <Link
                      to={urls.category(thread.category.parent)}
                      style={{
                        borderLeft: `4px solid ${thread.category.parent.color}`,
                      }}
                    >
                      {thread.category.parent.name}
                    </Link>
                  </li>
                )}
                <li className="list-inline-item">
                  <Link
                    to={urls.category(thread.category)}
                    style={{
                      borderLeft: `4px solid ${thread.category.color}`,
                    }}
                  >
                    {thread.category.name}
                  </Link>
                </li>
              </ul>
            </li>
          ))}
        </ul>
      ) : (
        <ThreadsListBlankslate category={category} />
      )}
      {loading && <CardLoader />}
    </ThreadsListCard>
  )
}
export default ThreadsList
