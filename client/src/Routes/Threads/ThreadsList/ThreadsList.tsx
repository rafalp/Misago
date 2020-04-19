import { ApolloError } from "apollo-client"
import React from "react"
import { Link } from "react-router-dom"
import { CardLoader } from "../../../UI"
import * as urls from "../../../urls"
import { IThread } from "../Threads.types"
import ThreadsListCard from "./ThreadsListCard"
import ThreadsListGraphQLError from "./ThreadsListGraphQLError"

interface IThreadsListProps {
  loading?: boolean
  error?: ApolloError | null
  threads: {
    items: Array<IThread>
    nextCursor: string | null
  } | null
}

const ThreadsList: React.FC<IThreadsListProps> = ({
  error,
  loading,
  threads,
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
      {threads ? (
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
        <div>No threads!</div>
      )}
    </ThreadsListCard>
  )
}
export default ThreadsList
