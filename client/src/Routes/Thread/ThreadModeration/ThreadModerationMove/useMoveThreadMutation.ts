import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../../types"
import { Thread, ThreadCategory } from "../../Thread.types"

const MOVE_THREADS = gql`
  mutation MoveThread($input: MoveThreadInput!) {
    moveThread(input: $input) {
      errors {
        message
        location
        type
      }
      thread {
        id
        category {
          id
          name
          slug
          color
          icon
          isClosed
          banner {
            full {
              align
              background
              height
              url
            }
            half {
              align
              background
              height
              url
            }
          }
          parent {
            id
            name
            slug
            color
            icon
          }
        }
      }
    }
  }
`

interface IMoveThreadMutationData {
  moveThread: {
    errors: Array<MutationError> | null
    thread: {
      id: string
      category: ThreadCategory
    } | null
  }
}

interface IMoveThreadMutationVariables {
  input: {
    thread: string
    category: string
  }
}

const useMoveThreadMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IMoveThreadMutationData,
    IMoveThreadMutationVariables
  >(MOVE_THREADS)

  return {
    data,
    error,
    loading,
    moveThread: (thread: Thread, category: string) => {
      return mutation({
        variables: {
          input: { category, thread: thread.id },
        },
      })
    },
  }
}

export default useMoveThreadMutation
