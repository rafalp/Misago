import { MutationResult } from "@apollo/react-common"
import { useMutation } from "@apollo/react-hooks"
import React from "react"
import gql from "graphql-tag"
import { useModalContext } from "../../../Context"
import { MutationError } from "../../../types"
import { Thread } from "../Thread.types"
import ThreadModerationClose from "./ThreadModerationClose"
import ThreadModerationOpen from "./ThreadModerationOpen"

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

interface CloseThreadMutationData {
  closeThread: {
    errors: Array<MutationError> | null
    thread: {
      id: string
      isClosed: boolean
    } | null
  }
}

interface CloseThreadMutationVariables {
  input: {
    thread: string
    isClosed: boolean
  }
}

const useCloseThreadMutation = (
  thread: Thread | null,
  isClosed: boolean
): [() => Promise<void>, MutationResult<CloseThreadMutationData>] => {
  const [mutation, state] = useMutation<
    CloseThreadMutationData,
    CloseThreadMutationVariables
  >(CLOSE_THREAD)

  const { openModal } = useModalContext()

  const runMutation = async () => {
    if (!thread) return

    const ErrorModal = isClosed ? ThreadModerationClose : ThreadModerationOpen

    try {
      const { data } = await mutation({
        variables: {
          input: {
            isClosed,
            thread: thread.id,
          },
        },
      })
      const errors = data?.closeThread.errors
      if (errors) {
        openModal(<ErrorModal errors={errors} />)
      }
    } catch (graphqlError) {
      openModal(<ErrorModal graphqlError={graphqlError} />)
    }
  }

  return [runMutation, state]
}

const useCloseThread = (thread: Thread | null) => {
  return useCloseThreadMutation(thread, true)
}

const useOpenThread = (thread: Thread | null) => {
  return useCloseThreadMutation(thread, false)
}

export { useCloseThread, useOpenThread }
