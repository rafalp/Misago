import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread, IThreadCategory } from "../Threads.types"

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

interface IMoveThreadsMutationData {
  moveThreads: {
    errors: Array<IMutationError> | null
    threads: Array<{
      id: string
      category: IThreadCategory
    }> | null
    updated: boolean
  }
}

interface IMoveThreadsMutationVariables {
  input: {
    threads: Array<string>
    category: string
  }
}

const useMoveThreadsMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IMoveThreadsMutationData,
    IMoveThreadsMutationVariables
  >(MOVE_THREADS)

  return {
    data,
    error,
    loading,
    moveThreads: (threads: Array<IThread>, category: string) => {
      return mutation({
        variables: {
          input: { category, threads: threads.map((thread) => thread.id) },
        },
      })
    },
  }
}

export default useMoveThreadsMutation
