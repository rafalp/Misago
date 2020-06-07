import { MutationResult } from "@apollo/react-common"
import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread } from "../Threads.types"
import { useThreadsModerationModalContext } from "./ThreadsModerationModalContext"

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

  const { closeThreads, openThreads } = useThreadsModerationModalContext(
    threads
  )

  const runMutation = async () => {
    const openErrorsModal = isClosed ? closeThreads : openThreads
    try {
      const { data } = await mutation()
      const { errors } = data?.closeThreads || { errors: null }
      if (errors) openErrorsModal({ errors })
    } catch (graphqlError) {
      openErrorsModal({ graphqlError })
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
