import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext, useModalContext } from "../../../Context"
import { ICategory } from "../../../types"
import { IThread, IThreadsModeration } from "../Threads.types"
import ThreadsModerationDelete from "./ThreadsModerationDelete"
import ThreadsModerationMove from "./ThreadsModerationMove"
import { useCloseThreads, useOpenThreads } from "./useCloseThreadsMutation"

const useThreadsModeration = (
  threads: Array<IThread>,
  category?: ICategory | null
): IThreadsModeration | null => {
  const user = useAuthContext()
  const { openModal } = useModalContext()

  const [closeThreads, { loading: closingThreads }] = useCloseThreads(threads)
  const [openThreads, { loading: openingThreads }] = useOpenThreads(threads)

  const moveThreads = () => {
    openModal(<ThreadsModerationMove threads={threads} />)
  }

  const deleteThreads = () => {
    openModal(
      <ThreadsModerationDelete threads={threads} category={category} />
    )
  }

  const moderation = {
    loading: closingThreads || openingThreads,
    disabled: threads.length === 0,
    actions: [
      {
        name: <Trans id="moderation.open">Open</Trans>,
        icon: "fas fa-unlock",
        action: openThreads,
      },
      {
        name: <Trans id="moderation.close">Close</Trans>,
        icon: "fas fa-lock",
        action: closeThreads,
      },
      {
        name: <Trans id="moderation.move">Move</Trans>,
        icon: "fas fa-arrow-right",
        action: moveThreads,
      },
      {
        name: <Trans id="moderation.delete">Delete</Trans>,
        icon: "fas fa-times",
        action: deleteThreads,
      },
    ],
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadsModeration
