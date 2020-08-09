import { Trans } from "@lingui/macro"
import React from "react"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface IThreadsModerationErrorHeaderProps {
  forDelete?: boolean
  threads?: Array<ISelectedThread>
  threadsErrors?: Record<string, IMutationError>
}

const ThreadsModerationErrorHeader: React.FC<IThreadsModerationErrorHeaderProps> = ({
  forDelete,
  threads,
  threadsErrors,
}) => {
  if (forDelete) {
    return (
      <ThreadsModerationErrorHeaderForDelete
        threads={threads}
        threadsErrors={threadsErrors}
      />
    )
  }

  return (
    <ThreadsModerationErrorHeaderForUpdate
      threads={threads}
      threadsErrors={threadsErrors}
    />
  )
}

const ThreadsModerationErrorHeaderForDelete: React.FC<IThreadsModerationErrorHeaderProps> = ({
  threads,
  threadsErrors,
}) => {
  const errorsCount = threadsErrors ? Object.keys(threadsErrors).length : 0

  if (threads) {
    if (threads.length === 1) {
      return (
        <Trans id="moderation.selected_thread_delete_error">
          Selected thread could not be deleted.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < threads.length) {
      return (
        <Trans id="moderation.selected_threads_delete_error_some">
          Some of the selected threads could not be deleted.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.selected_threads_delete_error">
      Selected threads could not be deleted.
    </Trans>
  )
}

const ThreadsModerationErrorHeaderForUpdate: React.FC<IThreadsModerationErrorHeaderProps> = ({
  threads,
  threadsErrors,
}) => {
  const errorsCount = threadsErrors ? Object.keys(threadsErrors).length : 0

  if (threads) {
    if (threads.length === 1) {
      return (
        <Trans id="moderation.selected_thread_delete">
          Selected thread could not be updated.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < threads.length) {
      return (
        <Trans id="moderation.selected_threads_error_some">
          Some of the selected threads could not be updated.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.selected_threads_error">
      Selected threads could not be updated.
    </Trans>
  )
}

export default ThreadsModerationErrorHeader
