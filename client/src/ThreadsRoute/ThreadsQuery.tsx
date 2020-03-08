import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import { ApolloError } from "apollo-client"
import React from "react"
import { RouteGraphQLError, RouteLoader, RouteNotFound } from "../UI"

const POLL_INTERVAL = 50 * 1000 // 50s

const THREADS_QUERY = gql`
  query ThreadsData {
    threads {
      items {
        id
        title
        slug
      }
      nextCursor
    }
  }
`

interface IThreadsQueryData {
  threads: {
    items: Array<IThreadData>
    nextCursor: string | null
  }
}

interface IThreadData {
  id: string
  title: string
  slug: string
}

interface IThreadsQueryProps {
  children: (props: IThreadsQueryChildrenProps) => React.ReactElement
}

interface IThreadsQueryChildrenProps {
  data: IThreadsQueryData
  error: ApolloError | undefined
  loading: boolean
}

const ThreadsQuery: React.FC<IThreadsQueryProps> = ({ children }) => {
  const { data, error, loading } = useQuery<IThreadsQueryData>(THREADS_QUERY, {
    pollInterval: POLL_INTERVAL,
  })

  if (!data) {
    if (loading) return <RouteLoader />
    if (error) return <RouteGraphQLError error={error} />
    return <RouteNotFound />
  }

  return children({ error, loading, data })
}

export default ThreadsQuery
