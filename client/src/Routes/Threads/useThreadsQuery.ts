import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import { IThread } from "./Threads.types"

const THREADS_FIELDS = `
  items {
    id
    title
    slug
    category {
      id
      name
      slug
      color
      icon
      parent {
        id
        name
        slug
        color
        icon
      }
    }
  }
  nextCursor
`

const THREADS_QUERY = gql`
  query Threads($cursor: ID) {
    threads(cursor: $cursor) {
      ${THREADS_FIELDS}
    }
  }
`

interface IThreadsData {
  threads: {
    items: Array<IThread>
    nextCursor: string | null
    __typename: string
  }
}

interface IThreadsVariables {
  cursor?: string | null
}

export const useThreadsQuery = () => {
  const result = useQuery<IThreadsData, IThreadsVariables>(THREADS_QUERY, {
    notifyOnNetworkStatusChange: true,
  })

  const fetchMoreThreads = () => {
    const cursor = result.data?.threads.nextCursor
    if (!cursor) return

    result.fetchMore({
      query: THREADS_QUERY,
      variables: { cursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult) return previousResult

        return fetchMoreResult
          ? {
              threads: {
                items: [
                  ...previousResult.threads.items,
                  ...fetchMoreResult.threads.items,
                ],
                nextCursor: fetchMoreResult.threads.nextCursor,
                __typename: previousResult.threads.__typename,
              },
            }
          : previousResult
      },
    })
  }

  return { ...result, fetchMoreThreads }
}

interface ICategoryQueryParams {
  id: string
}

const CATEGORY_THREADS_QUERY = gql`
  query CategoryThreads($id: ID!, $cursor: ID) {
    category(id: $id) {
      id
      name
      slug
      parent {
        id
        name
        slug
      }
    }
    threads(category: $id, cursor: $cursor) {
      ${THREADS_FIELDS}
    }
  }
`

interface ICategoryThreadsData extends IThreadsData {
  category: {
    id: string
    name: string
    slug: string
    color: string | null
    icon: string | null
    parent: {
      id: string
      name: string
      slug: string
      color: string | null
      icon: string | null
    } | null
  }
}

interface ICategoryVariables extends IThreadsVariables {
  id: string
}

export const useCategoryThreadsQuery = (variables: ICategoryQueryParams) => {
  const result = useQuery<ICategoryThreadsData, ICategoryVariables>(
    CATEGORY_THREADS_QUERY,
    { variables, notifyOnNetworkStatusChange: true }
  )

  const fetchMoreThreads = () => {
    const cursor = result.data?.threads.nextCursor
    if (!cursor) return

    result.fetchMore({
      query: CATEGORY_THREADS_QUERY,
      variables: { ...variables, cursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        if (!fetchMoreResult) return previousResult

        return fetchMoreResult
          ? {
              category: fetchMoreResult.category,
              threads: {
                items: [
                  ...previousResult.threads.items,
                  ...fetchMoreResult.threads.items,
                ],
                nextCursor: fetchMoreResult.threads.nextCursor,
                __typename: previousResult.threads.__typename,
              },
            }
          : previousResult
      },
    })
  }

  return { ...result, fetchMoreThreads }
}
