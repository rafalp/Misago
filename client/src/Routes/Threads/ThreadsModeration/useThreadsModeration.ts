import React from "react"
import { useAuthContext } from "../../../Context"
import { IThread, IThreadsModeration } from "../Threads.types"
import { useCloseThreads, useOpenThreads } from "./closeThreads"

const useThreadsModeration = (
  threads: Array<IThread>
): IThreadsModeration | null => {
  const user = useAuthContext()
  const closeThreads = useCloseThreads(threads)
  const openThreads = useOpenThreads(threads)

  const moderation = {
    disabled: threads.length === 0,
    closeThreads,
    openThreads,
    moveThreads: () => console.log("CLOSE THREADS"),
    deleteThreads: () => console.log("CLOSE THREADS"),
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadsModeration
