import React from "react"
import { Link } from "react-router-dom"
import ThreadsQuery from "./ThreadsQuery"

const ThreadsRoute: React.FC = () => (
  <ThreadsQuery>
    {({ data }) => (
      <div>
        <ul>
          {data.threads.items.map(thread => (
            <li key={thread.id}>
              <Link to={`/t/${thread.slug}/${thread.id}/`}>{thread.title}</Link>
            </li>
          ))}
        </ul>
      </div>
    )}
  </ThreadsQuery>
)

export default ThreadsRoute
