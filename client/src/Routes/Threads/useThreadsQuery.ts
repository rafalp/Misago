import { useQuery, useSubscription } from "@apollo/react-hooks"
import { DocumentNode } from "graphql"
import gql from "graphql-tag"
import React from "react"
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

const THREADS_UPDATES_SUBSCRIPTION = gql`
  subscription ThreadsUpdates {
    threads
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

interface IThreadsUpdatesData {
  threads: string
}

export const useBaseThreadsQuery = <
  TData extends IThreadsData,
  TVariables extends IThreadsVariables
>(
  query: DocumentNode,
  variables?: TVariables
) => {
  const result = useQuery<TData, TVariables>(query, {
    variables,
    fetchPolicy: "cache-and-network",
    notifyOnNetworkStatusChange: true,
  })

  const fetchMoreThreads = () => {
    const cursor = result.data?.threads.nextCursor
    if (!cursor) return

    result.fetchMore({
      query: THREADS_QUERY,
      variables: { cursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        return mergeThreadsResults(previousResult, fetchMoreResult)
      },
    })
  }

  const [updatedThreads, setUpdatedThreadsState] = React.useState<{
    ids: Array<string>
    length: number
  }>({ ids: [], length: 0 })

  useSubscription<IThreadsUpdatesData>(THREADS_UPDATES_SUBSCRIPTION, {
    shouldResubscribe: !!result.data?.threads,
    onSubscriptionData: ({ subscriptionData: { data } }) => {
      if (!data) return
      const { threads: id } = data
      if (updatedThreads.ids.indexOf(id) !== -1) return

      setUpdatedThreadsState((state) => {
        return {
          ids: [...state.ids, id],
          length: state.length + 1,
        }
      })
    },
  })

  return { ...result, fetchMoreThreads, updatedThreads: updatedThreads.length }
}

const mergeThreadsResults = <TData extends IThreadsData>(
  previousResult: TData,
  fetchMoreResult?: TData
) => {
  if (!fetchMoreResult) return previousResult

  return {
    ...previousResult,
    threads: {
      items: [
        ...previousResult.threads.items,
        ...fetchMoreResult.threads.items,
      ],
      nextCursor: fetchMoreResult.threads.nextCursor,
      __typename: previousResult.threads.__typename,
    },
  }
}

export const useThreadsQuery = () => {
  return useBaseThreadsQuery<IThreadsData, IThreadsVariables>(THREADS_QUERY)
}

interface ICategoryQueryParams {
  id: string
}

const CATEGORY_THREADS_QUERY = gql`
  fragment CategoryFields on Category {
    id
    name
    slug
  }

  query CategoryThreads($id: ID!, $cursor: ID) {
    category(id: $id) {
      ...CategoryFields
      threads
      posts
      parent {
        ...CategoryFields
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
    threads: number
    posts: number
    parent: {
      id: string
      name: string
      slug: string
    } | null
  }
}

interface ICategoryVariables extends IThreadsVariables {
  id: string
}

export const useCategoryThreadsQuery = (variables: ICategoryQueryParams) => {
  return useBaseThreadsQuery<ICategoryThreadsData, ICategoryVariables>(
    CATEGORY_THREADS_QUERY,
    variables
  )
}
