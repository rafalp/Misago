import { MutationResult } from "@apollo/react-common"
import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import React from "react"
import { useModalContext } from "../../../Context"
import { MutationError } from "../../../types"
import { IThread } from "../Threads.types"
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

interface ICloseThreadsMutationData {
  closeThreads: {
    errors: Array<MutationError> | null
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

const useCloseThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, true)
}

const useOpenThreads = (threads: Array<IThread>) => {
  return useCloseThreadsMutation(threads, false)
}

export { useCloseThreads, useOpenThreads }
