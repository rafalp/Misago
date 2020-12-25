import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../../types"
import { Thread } from "../../Thread.types"

const DELETE_THREAD = gql`
  mutation DeleteThread($input: DeleteThreadInput!) {
    deleteThread(input: $input) {
      errors {
        message
        location
        type
      }
    }
  }
`

interface IDeleteThreadMutationData {
  deleteThread: {
    errors: Array<MutationError> | null
  }
}

interface IDeleteThreadMutationVariables {
  input: {
    thread: string
  }
}

const useDeleteThreadMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IDeleteThreadMutationData,
    IDeleteThreadMutationVariables
  >(DELETE_THREAD)

  return {
    data,
    error,
    loading,
    deleteThread: (thread: Thread) => {
      return mutation({
        variables: {
          input: { thread: thread.id },
        },
      })
    },
  }
}

export default useDeleteThreadMutation
