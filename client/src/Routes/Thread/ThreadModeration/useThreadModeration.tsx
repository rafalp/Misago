import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { IThread, IThreadModeration } from "../Thread.types"
import { useCloseThread, useOpenThread } from "./closeThread"

const useThreadModeration = (thread: IThread): IThreadModeration | null => {
  const user = useAuthContext()

  const [closeThread, { loading: closingThread }] = useCloseThread(thread)
  const [openThread, { loading: openingThread }] = useOpenThread(thread)
  const moveThread = () => {}
  const deleteThread = () => {}

  const moderation = {
    loading: closingThread || openingThread,
    closeThread,
    openThread,
    moveThread,
    deleteThread,
    actions: [
      {
        name: <Trans id="moderation.open">Open</Trans>,
        icon: "unlock",
        iconSolid: true,
        disabled: !thread.isClosed,
        action: openThread,
      },
      {
        name: <Trans id="moderation.close">Close</Trans>,
        icon: "lock",
        iconSolid: true,
        disabled: thread.isClosed,
        action: closeThread,
      },
      {
        name: <Trans id="moderation.move">Move</Trans>,
        icon: "arrow-right",
        iconSolid: true,
        action: moveThread,
      },
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "times",
        iconSolid: true,
        action: deleteThread,
      },
    ],
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadModeration
