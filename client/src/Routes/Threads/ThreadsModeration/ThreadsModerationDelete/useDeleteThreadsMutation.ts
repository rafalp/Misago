import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { getSelectionErrors } from "../../../../UI/useSelectionErrors"
import { Category, MutationError } from "../../../../types"
import { Thread } from "../../Threads.types"
import {
  CATEGORY_THREADS_QUERY,
  THREADS_QUERY,
  ThreadsData,
} from "../../useThreadsQuery"

const THREAD_NOT_EXISTS = "value_error.thread.not_exists"

const DELETE_THREADS = gql`
  mutation DeleteThreads($input: BulkDeleteThreadsInput!) {
    deleteThreads(input: $input) {
      errors {
        message
        location
        type
      }
      deleted
    }
  }
`

interface DeleteThreadsMutationData {
  deleteThreads: {
    errors: Array<MutationError> | null
    deleted: Array<string>
  }
}

interface DeleteThreadsMutationVariables {
  input: {
    threads: Array<string>
  }
}

const useDeleteThreadsMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    DeleteThreadsMutationData,
    DeleteThreadsMutationVariables
  >(DELETE_THREADS)

  return {
    data,
    error,
    loading,
    deleteThreads: (threads: Array<Thread>, category?: Category | null) => {
      const deletedThreadsIds = threads.map((thread) => thread.id)
      return mutation({
        variables: {
          input: { threads: deletedThreadsIds },
        },
        update: (cache, { data }) => {
          if (!data || !data.deleteThreads) return

          const errors = getSelectionErrors<Thread>(
            "threads",
            threads,
            data.deleteThreads.errors || []
          )

          let queryID = category
            ? {
                query: CATEGORY_THREADS_QUERY,
                variables: { category: category.id },
              }
            : {
                query: THREADS_QUERY,
              }

          const query = cache.readQuery<ThreadsData>(queryID)
          if (!query) return null

          cache.writeQuery<ThreadsData>({
            ...queryID,
            data: {
              ...query,
              threads: {
                ...query.threads,
                items: query.threads.items.filter((thread) => {
                  if (
                    errors[thread.id] &&
                    errors[thread.id].type !== THREAD_NOT_EXISTS
                  ) {
                    return true
                  }

                  return data.deleteThreads.deleted.indexOf(thread.id) < 0
                }),
              },
            },
          })
        },
      })
    },
  }
}

export default useDeleteThreadsMutation
