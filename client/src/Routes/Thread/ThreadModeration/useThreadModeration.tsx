import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { IThread, IThreadModeration } from "../Thread.types"

const useThreadModeration = (
  thread: IThread | null
): IThreadModeration | null => {
  const user = useAuthContext()

  if (!thread) return null

  const closeThread = () => {}
  const openThread = () => {}
  const moveThread = () => {}
  const deleteThread = () => {}

  const moderation = {
    loading: false,
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
