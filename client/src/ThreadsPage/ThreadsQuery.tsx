import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import { ApolloError } from "apollo-client"
import React from "react"
import { PageLoader } from "../UI"

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

interface IThreadsData {
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
  data: IThreadsData
  error: ApolloError | undefined
  loading: boolean
}

const ThreadsQuery: React.FC<IThreadsQueryProps> = ({ children }) => {
  const { data, error, loading } = useQuery<IThreadsData>(THREADS_QUERY, {
    pollInterval: POLL_INTERVAL,
  })

  if (!data) {
    if (loading) return <PageLoader />
    if (error) return <div>ERROR</div>
    return <div>ERROR</div>
  }

  return children({ error, loading, data })
}

export default ThreadsQuery
