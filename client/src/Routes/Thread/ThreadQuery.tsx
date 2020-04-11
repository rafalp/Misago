import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import { ApolloError } from "apollo-client"
import React from "react"
import { RouteGraphQLError, RouteLoader, RouteNotFound } from "../../UI"

const POLL_INTERVAL = 50 * 1000 // 50s

const THREAD_QUERY = gql`
  query Thread($id: ID!) {
    thread(id: $id) {
      id
      title
      slug
    }
  }
`

interface IThreadQueryData {
  thread: IThreadData | null
}

interface IThreadData {
  id: string
  title: string
  slug: string
}

interface IThreadQueryProps {
  id: string
  children: (props: IThreadQueryChildrenProps) => React.ReactElement
}

interface IThreadQueryChildrenProps {
  data: { thread: IThreadData }
  error: ApolloError | undefined
  loading: boolean
}

const ThreadQuery: React.FC<IThreadQueryProps> = ({ children, id }) => {
  const { data, error, loading } = useQuery<IThreadQueryData>(THREAD_QUERY, {
    pollInterval: POLL_INTERVAL,
    variables: { id },
  })

  if (!data) {
    if (loading) return <RouteLoader />
    if (error) return <RouteGraphQLError error={error} />
  }

  if (!data || !data.thread) {
    return <RouteNotFound />
  }

  return children({ error, loading, data: { thread: data.thread } })
}

export default ThreadQuery
