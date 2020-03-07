import React from "react"
import ThreadsQuery from "./ThreadsQuery"

const ThreadsRoute: React.FC = () => (
  <ThreadsQuery>
    {({ data }) => (
      <ul>
        {data.threads.items.map(thread => (
          <li key={thread.id}>
            <a href={`/t/${thread.slug}/${thread.id}/`}>{thread.title}</a>
          </li>
        ))}
      </ul>
    )}
  </ThreadsQuery>
)

export default ThreadsRoute
