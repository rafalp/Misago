import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../Context"
import { IThread, IThreadModeration } from "../Thread.types"
import ThreadModerationDelete from "./ThreadModerationDelete"
import ThreadModerationMove from "./ThreadModerationMove"
import { useCloseThread, useOpenThread } from "./closeThread"

const useThreadModeration = (
  thread: IThread | null
): IThreadModeration | null => {
  const user = useAuthContext()
  const { openModal } = useModalContext()

  const [closeThread, { loading: closingThread }] = useCloseThread(thread)
  const [openThread, { loading: openingThread }] = useOpenThread(thread)

  if (!thread || !user || !user.isModerator) return null

  const moveThread = () => openModal(<ThreadModerationMove thread={thread} />)
  const deleteThread = () =>
    openModal(<ThreadModerationDelete thread={thread} />)

  return {
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
}

export default useThreadModeration
