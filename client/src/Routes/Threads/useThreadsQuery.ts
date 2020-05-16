import { useLazyQuery, useQuery, useSubscription } from "@apollo/react-hooks"
import { DocumentNode } from "graphql"
import gql from "graphql-tag"
import React from "react"
import { IThread } from "./Threads.types"

const THREADS_FRAGMENTS = `
  fragment ThreadsListThreadPoster on User {
    id
    name
    slug
    avatars {
      size
      url
    }
  }

  fragment ThreadsListThreadCategory on Category {
    id
    name
    slug
    color
    icon
  }
`

const THREADS_FIELDS = `
  items {
    id
    title
    slug
    startedAt
    lastPostedAt
    replies
    isClosed
    starterName
    lastPosterName
    starter {
      ...ThreadsListThreadPoster
    }
    lastPoster {
      ...ThreadsListThreadPoster
    }
    category {
      ...ThreadsListThreadCategory
      parent {
        ...ThreadsListThreadCategory
      }
    }
  }
  nextCursor
`

const THREADS_QUERY = gql`
  ${THREADS_FRAGMENTS}

  query Threads($cursor: ID) {
    threads(cursor: $cursor) {
      ${THREADS_FIELDS}
    }
  }
`

const THREADS_UPDATES_SUBSCRIPTION = gql`
  subscription ThreadsUpdates($category: ID) {
    threads(category: $category)
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
  category?: string | null
  cursor?: string | null
}

interface IThreadsUpdatesData {
  threads: string
}

interface IThreadsUpdatesVariables {
  category?: string | null
}

export const useBaseThreadsQuery = <TData extends IThreadsData>(
  query: DocumentNode,
  variables?: IThreadsVariables
) => {
  const result = useQuery<TData, IThreadsVariables>(query, {
    variables,
    fetchPolicy: "cache-and-network",
    notifyOnNetworkStatusChange: true,
  })

  const fetchMoreThreads = () => {
    const cursor = result.data?.threads.nextCursor
    if (!cursor) return

    result.fetchMore({
      query: THREADS_QUERY,
      variables: { ...variables, cursor },
      updateQuery: (previousResult, { fetchMoreResult }) => {
        return mergeMergeThreadsResults(previousResult, fetchMoreResult)
      },
    })
  }

  const [updatedThreads, setUpdatedThreadsState] = React.useState<{
    ids: Array<string>
    length: number
  }>({ ids: [], length: 0 })

  useSubscription<IThreadsUpdatesData, IThreadsUpdatesVariables>(
    THREADS_UPDATES_SUBSCRIPTION,
    {
      shouldResubscribe: !!result.data?.threads,
      variables: variables ? { category: variables.category } : undefined,
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
    }
  )

  const [fetchUpdatedThreads, updateResult] = useLazyQuery<
    TData,
    IThreadsVariables
  >(query, {
    fetchPolicy: "no-cache",
    notifyOnNetworkStatusChange: true,
    variables: variables ? { category: variables.category } : undefined,
    onCompleted: (data) => {
      setUpdatedThreadsState({
        ids: [],
        length: 0,
      })

      result.updateQuery((previousResult) => {
        return mergeUpdatedThreadsResults(previousResult, data)
      })
    },
  })

  return {
    ...result,
    fetchMoreThreads,
    fetchUpdatedThreads,
    updatedThreads: updatedThreads.length,
    updatingThreads: updateResult.loading,
    update: {
      threads: updatedThreads.length,
      loading: updateResult.loading,
      fetch: fetchUpdatedThreads,
    },
  }
}

const mergeMergeThreadsResults = <TData extends IThreadsData>(
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

const mergeUpdatedThreadsResults = <TData extends IThreadsData>(
  previousResult: TData,
  updatedResult: TData
) => {
  const updatedIds = updatedResult.threads.items.map(({ id }) => id)
  const items = [
    ...updatedResult.threads.items,
    ...previousResult.threads.items.filter(
      ({ id }) => updatedIds.indexOf(id) === -1
    ),
  ]

  return {
    ...updatedResult,
    threads: {
      items,
      nextCursor: previousResult.threads.nextCursor,
      __typename: previousResult.threads.__typename,
    },
  }
}

export const useThreadsQuery = () => {
  return useBaseThreadsQuery<IThreadsData>(THREADS_QUERY)
}

interface ICategoryQueryParams {
  id: string
}

const CATEGORY_THREADS_QUERY = gql`
  ${THREADS_FRAGMENTS}

  fragment ThreadsListCategory on Category {
    id
    name
    slug
  }

  query CategoryThreads($category: ID!, $cursor: ID) {
    category(id: $category) {
      ...ThreadsListCategory
      threads
      posts
      parent {
        ...ThreadsListCategory
      }
    }
    threads(category: $category, cursor: $cursor) {
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

export const useCategoryThreadsQuery = (variables: ICategoryQueryParams) => {
  return useBaseThreadsQuery<ICategoryThreadsData>(CATEGORY_THREADS_QUERY, {
    category: variables.id,
  })
}
