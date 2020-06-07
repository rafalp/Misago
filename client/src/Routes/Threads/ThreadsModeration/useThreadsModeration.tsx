import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { ICategory } from "../../../types"
import { IThread, IThreadsModeration } from "../Threads.types"
import { useThreadsModerationModalContext } from "./ThreadsModerationModalContext"
import { useCloseThreads, useOpenThreads } from "./closeThreads"

const useThreadsModeration = (
  threads: Array<IThread>,
  category?: ICategory | null
): IThreadsModeration | null => {
  const user = useAuthContext()

  const [closeThreads] = useCloseThreads(threads)
  const [openThreads] = useOpenThreads(threads)
  const { moveThreads, deleteThreads } = useThreadsModerationModalContext(
    threads,
    category
  )

  const moderation = {
    disabled: threads.length === 0,
    closeThreads,
    openThreads,
    moveThreads,
    deleteThreads,
    actions: [
      {
        name: <Trans id="moderation.open">Open</Trans>,
        icon: "unlock",
        iconSolid: true,
        action: openThreads,
      },
      {
        name: <Trans id="moderation.close">Close</Trans>,
        icon: "lock",
        iconSolid: true,
        action: closeThreads,
      },
      {
        name: <Trans id="moderation.move">Move</Trans>,
        icon: "arrow-right",
        iconSolid: true,
        action: moveThreads,
      },
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "times",
        iconSolid: true,
        action: deleteThreads,
      },
    ],
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadsModeration
