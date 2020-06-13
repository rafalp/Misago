import { MutationResult } from "@apollo/react-common"
import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IThread } from "../Thread.types"
import { useThreadModerationModalContext } from "./ThreadModerationModalContext"

const CLOSE_THREAD = gql`
  mutation CloseThread($input: CloseThreadInput!) {
    closeThread(input: $input) {
      errors {
        message
        location
        type
      }
      thread {
        id
        isClosed
      }
    }
  }
`

interface ICloseThreadMutationData {
  closeThread: {
    errors: Array<IMutationError> | null
    thread: {
      id: string
      isClosed: boolean
    } | null
  }
}

interface ICloseThreadMutationVariables {
  input: {
    thread: string
    isClosed: boolean
  }
}

const useCloseThreadMutation = (
  thread: IThread,
  isClosed: boolean
): [() => Promise<void>, MutationResult<ICloseThreadMutationData>] => {
  const [mutation, state] = useMutation<
    ICloseThreadMutationData,
    ICloseThreadMutationVariables
  >(CLOSE_THREAD, {
    variables: {
      input: {
        isClosed,
        thread: thread.id,
      },
    },
  })

  const { closeThread, openThread } = useThreadModerationModalContext(thread)

  const runMutation = async () => {
    const openErrorsModal = isClosed ? closeThread : openThread
    try {
      const { data } = await mutation()
      const { errors } = data?.closeThread || { errors: null }
      if (errors) openErrorsModal({ errors })
    } catch (graphqlError) {
      openErrorsModal({ graphqlError })
    }
  }

  return [runMutation, state]
}

const useCloseThread = (thread: IThread) => {
  return useCloseThreadMutation(thread, true)
}

const useOpenThread = (thread: IThread) => {
  return useCloseThreadMutation(thread, false)
}

export { useCloseThread, useOpenThread }
