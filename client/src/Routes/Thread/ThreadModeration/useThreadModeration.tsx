import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../Context"
import { Thread, ThreadModerationOptions } from "../Thread.types"
import ThreadModerationDelete from "./ThreadModerationDelete"
import ThreadModerationMove from "./ThreadModerationMove"
import { useCloseThread, useOpenThread } from "./useCloseThreadMutation"

const useThreadModeration = (
  thread: Thread | null
): ThreadModerationOptions | null => {
  const user = useAuthContext()
  const { openModal } = useModalContext()

  const [closeThread, { loading: closingThread }] = useCloseThread(thread)
  const [openThread, { loading: openingThread }] = useOpenThread(thread)

  if (!thread || !user || !user.isModerator) return null

  const moveThread = () => openModal(<ThreadModerationMove thread={thread} />)
  const deleteThread = () => {
    openModal(<ThreadModerationDelete thread={thread} />)
  }

  return {
    loading: closingThread || openingThread,
    actions: [
      {
        name: <Trans id="moderation.open">Open</Trans>,
        icon: "fas fa-unlock",
        disabled: !thread.isClosed,
        action: openThread,
      },
      {
        name: <Trans id="moderation.close">Close</Trans>,
        icon: "fas fa-lock",
        disabled: thread.isClosed,
        action: closeThread,
      },
      {
        name: <Trans id="moderation.move">Move</Trans>,
        icon: "fas fa-arrow-right",
        action: moveThread,
      },
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "fas fa-times",
        action: deleteThread,
      },
    ],
  }
}

export default useThreadModeration
