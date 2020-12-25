import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../../types"
import { Thread, ThreadCategory } from "../../Threads.types"

const MOVE_THREADS = gql`
  mutation MoveThreads($input: BulkMoveThreadsInput!) {
    moveThreads(input: $input) {
      errors {
        message
        location
        type
      }
      threads {
        id
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
      updated
    }
  }
`

interface MoveThreadsMutationData {
  moveThreads: {
    errors: Array<MutationError> | null
    threads: Array<{
      id: string
      category: ThreadCategory
    }> | null
    updated: boolean
  }
}

interface MoveThreadsMutationVariables {
  input: {
    threads: Array<string>
    category: string
  }
}

const useMoveThreadsMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    MoveThreadsMutationData,
    MoveThreadsMutationVariables
  >(MOVE_THREADS)

  return {
    data,
    error,
    loading,
    moveThreads: (threads: Array<Thread>, category: string) => {
      return mutation({
        variables: {
          input: { category, threads: threads.map((thread) => thread.id) },
        },
      })
    },
  }
}

export default useMoveThreadsMutation
