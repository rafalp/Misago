import { useAuthContext } from "../../../Context"
import { IThread, IThreadsModeration } from "../Threads.types"
import { useThreadModerationModalContext } from "./ThreadsModerationModalContext"
import { useCloseThreads, useOpenThreads } from "./closeThreads"

const useThreadsModeration = (
  threads: Array<IThread>
): IThreadsModeration | null => {
  const user = useAuthContext()

  const closeThreads = useCloseThreads(threads)
  const openThreads = useOpenThreads(threads)
  const { moveThreads, deleteThreads } = useThreadModerationModalContext(
    threads
  )

  const moderation = {
    disabled: threads.length === 0,
    closeThreads,
    openThreads,
    moveThreads,
    deleteThreads,
  }

  if (user && user.isModerator) return moderation
  return null
}

export default useThreadsModeration
