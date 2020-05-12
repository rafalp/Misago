import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread } from "../Threads.types"

const CLOSE_THREADS = gql`
  mutation CloseThreads($input: BulkCloseThreadsInput!) {
    closeThreads(input: $input) {
      errors {
        message
        location
        type
      }
      threads {
        id
        isClosed
      }
    }
  }
`

interface ICloseThreadsMutationData {
  closeThreads: {
    errors: Array<IMutationError> | null
    threads: Array<{
      id: string
      isClosed: boolean
    }> | null
  }
}

interface ICloseThreadsMutationVariables {
  input: {
    threads: Array<string>
    isClosed: boolean
  }
}

const useCloseThreadsMutation = (
  threads: Array<IThread>,
  isClosed: boolean
) => {
  const [mutation] = useMutation<
    ICloseThreadsMutationData,
    ICloseThreadsMutationVariables
  >(CLOSE_THREADS, {
    variables: {
      input: {
        isClosed,
        threads: threads.map((thread) => thread.id),
      },
    },
  })

  return mutation
}

const useCloseThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, true)
}

const useOpenThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, false)
}

export { useCloseThreads, useOpenThreads }
