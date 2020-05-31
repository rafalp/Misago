import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread } from "../Threads.types"

const DELETE_THREADS = gql`
  mutation DeleteThreads($input: BulkDeleteThreadsInput!) {
    deleteThreads(input: $input) {
      errors {
        message
        location
        type
      }
    }
  }
`

interface IDeleteThreadsMutationData {
  deleteThreads: {
    errors: Array<IMutationError> | null
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
    deleteThreads: (threads: Array<IThread>) => {
      return mutation({
        variables: {
          input: { threads: threads.map((thread) => thread.id) },
        },
      })
    },
  }
}

export default useDeleteThreadsMutation
