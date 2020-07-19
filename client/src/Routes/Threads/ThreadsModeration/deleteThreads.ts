import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { getSelectionErrors } from "../../../UI"
import { ICategory, IMutationError } from "../../../types"
import { IThread } from "../Threads.types"
import {
  CATEGORY_THREADS_QUERY,
  THREADS_QUERY,
  IThreadsData,
} from "../useThreadsQuery"

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

interface IDeleteThreadsMutationData {
  deleteThreads: {
    errors: Array<IMutationError> | null
    deleted: boolean
  }
}

interface IDeleteThreadsMutationVariables {
  input: {
    threads: Array<string>
  }
}

const useDeleteThreadsMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IDeleteThreadsMutationData,
    IDeleteThreadsMutationVariables
  >(DELETE_THREADS)

  return {
    data,
    error,
    loading,
    deleteThreads: (threads: Array<IThread>, category?: ICategory | null) => {
      const deletedThreads = threads.map((thread) => thread.id)
      return mutation({
        variables: {
          input: { threads: deletedThreads },
        },
        update: (cache, { data }) => {
          if (!data || !data.deleteThreads) return

          const errors = getSelectionErrors<IThread>(
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

          const query = cache.readQuery<IThreadsData>(queryID)
          if (!query) return null

          cache.writeQuery<IThreadsData>({
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

                  return deletedThreads.indexOf(thread.id) < 0
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
