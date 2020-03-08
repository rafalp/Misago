import React from "react"
import { Link } from "react-router-dom"
import * as urls from "../urls"
import ThreadsQuery from "./ThreadsQuery"

const ThreadsRoute: React.FC = () => (
  <ThreadsQuery>
    {({ data }) => (
      <div>
        <Link to={urls.startThread()}>[START THREAD]</Link>
        <ul>
          {data.threads.items.map(thread => (
            <li key={thread.id}>
              <Link to={urls.thread(thread)}>{thread.title}</Link>
            </li>
          ))}
        </ul>
      </div>
    )}
  </ThreadsQuery>
)

export default ThreadsRoute
