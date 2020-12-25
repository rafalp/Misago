import { MutationResult } from "@apollo/react-common"
import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import React from "react"
import { useModalContext } from "../../../Context"
import { MutationError } from "../../../types"
import { Thread } from "../Threads.types"
import ThreadsModerationClose from "./ThreadsModerationClose"
import ThreadsModerationOpen from "./ThreadsModerationOpen"

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

interface CloseThreadsMutationData {
  closeThreads: {
    errors: Array<MutationError> | null
    threads: Array<{
      id: string
      isClosed: boolean
    }> | null
    updated: boolean
  }
}

interface CloseThreadsMutationVariables {
  input: {
    threads: Array<string>
    isClosed: boolean
  }
}

const useCloseThreadsMutation = (
  threads: Array<Thread>,
  isClosed: boolean
): [() => Promise<void>, MutationResult<CloseThreadsMutationData>] => {
  const [mutation, state] = useMutation<
    CloseThreadsMutationData,
    CloseThreadsMutationVariables
  >(CLOSE_THREADS, {
    variables: {
      input: {
        isClosed,
        threads: threads.map((thread) => thread.id),
      },
    },
  })

  const { openModal } = useModalContext()

  const runMutation = async () => {
    const ErrorModal = isClosed
      ? ThreadsModerationClose
      : ThreadsModerationOpen

    try {
      const { data } = await mutation()
      const errors = data?.closeThreads.errors
      if (errors) {
        openModal(<ErrorModal threads={threads} errors={errors} />)
      }
    } catch (graphqlError) {
      openModal(<ErrorModal threads={threads} graphqlError={graphqlError} />)
    }
  }

  return [runMutation, state]
}

const useCloseThreads = (threads: Array<Thread>) => {
  return useCloseThreadsMutation(threads, true)
}

const useOpenThreads = (threads: Array<Thread>) => {
  return useCloseThreadsMutation(threads, false)
}

export { useCloseThreads, useOpenThreads }
