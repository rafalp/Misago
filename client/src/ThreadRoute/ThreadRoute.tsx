import React from "react"
import { useParams } from "react-router-dom"
import { WindowTitle } from "../UI"
import ThreadQuery from "./ThreadQuery"

interface IThreadRouteParams {
  id: string
}

const ThreadRoute: React.FC = () => {
  const { id } = useParams<IThreadRouteParams>()

  return (
    <ThreadQuery id={id}>
      {({ data: { thread } }) => (
        <>
          <WindowTitle title={thread.title} />
          <h1>{thread.title}</h1>
        </>
      )}
    </ThreadQuery>
  )
}

export default ThreadRoute
