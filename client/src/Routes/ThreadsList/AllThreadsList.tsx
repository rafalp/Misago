import React from "react"
import { Link } from "react-router-dom"
import { RouteGraphQLError, RouteLoader } from "../../UI"
import * as urls from "../../urls"
import { useThreadsQuery } from "./useThreadsQuery"

const AllThreadsList: React.FC = () => {
  const { data, error, loading } = useThreadsQuery()

  if (loading) return <RouteLoader />
  if (error) return <RouteGraphQLError error={error} />

  return (
    <div>
      <Link to={urls.categories()}>[CATEGORIES]</Link>
      <Link to={urls.startThread()}>[START THREAD]</Link>
      <h1>[All threads]</h1>
      <ul>
        {data?.threads.items.map(thread => (
          <li key={thread.id}>
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
                  style={{ borderLeft: `4px solid ${thread.category.color}` }}
                >
                  {thread.category.name}
                </Link>
              </li>
            </ul>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default AllThreadsList
