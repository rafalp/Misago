import { Trans } from "@lingui/macro"
import React from "react"
import { IMutationError } from "../../../../types"
import { ISelectedThread } from "../../Threads.types"

interface IThreadsModerationModalErrorHeaderProps {
  forDelete?: boolean
  threads?: Array<ISelectedThread>
  threadsErrors?: Record<string, IMutationError>
}

const ThreadsModerationModalErrorHeader: React.FC<IThreadsModerationModalErrorHeaderProps> = ({
  forDelete,
  threads,
  threadsErrors,
}) => {
  if (forDelete) {
    return (
      <ThreadsModerationModalErrorHeaderForDelete
        threads={threads}
        threadsErrors={threadsErrors}
      />
    )
  }

  return (
    <ThreadsModerationModalErrorHeaderForUpdate
      threads={threads}
      threadsErrors={threadsErrors}
    />
  )
}

const ThreadsModerationModalErrorHeaderForDelete: React.FC<IThreadsModerationModalErrorHeaderProps> = ({
  threads,
  threadsErrors,
}) => {
  const errorsCount = threadsErrors ? Object.keys(threadsErrors).length : 0

  if (threads) {
    if (threads.length === 1) {
      return (
        <Trans id="moderation.thread_delete_error_header">
          Selected thread could not be deleted.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < threads.length) {
      return (
        <Trans id="moderation.threads_delete_error_header_some">
          Some of the selected threads could not be deleted.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.threads_delete_error_header">
      Selected threads could not be deleted.
    </Trans>
  )
}

const ThreadsModerationModalErrorHeaderForUpdate: React.FC<IThreadsModerationModalErrorHeaderProps> = ({
  threads,
  threadsErrors,
}) => {
  const errorsCount = threadsErrors ? Object.keys(threadsErrors).length : 0

  if (threads) {
    if (threads.length === 1) {
      return (
        <Trans id="moderation.thread_error_header">
          Selected thread could not be updated.
        </Trans>
      )
    } else if (errorsCount > 0 && errorsCount < threads.length) {
      return (
        <Trans id="moderation.threads_error_header_some">
          Some of the selected threads could not be updated.
        </Trans>
      )
    }
  }

  return (
    <Trans id="moderation.threads_error_header">
      Selected threads could not be updated.
    </Trans>
  )
}

export default ThreadsModerationModalErrorHeader
