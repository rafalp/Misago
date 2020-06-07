import { MutationResult } from "@apollo/react-common"
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
      updated
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
    updated: boolean
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
): [() => Promise<void>, MutationResult<ICloseThreadsMutationData>] => {
  const [mutation, state] = useMutation<
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

  const runMutation = async () => {
    try {
      await mutation()
    } catch (error) {
      console.warn(error)
    }
  }

  return [runMutation, state]
}

const useCloseThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, true)
}

const useOpenThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, false)
}

export { useCloseThreads, useOpenThreads }
