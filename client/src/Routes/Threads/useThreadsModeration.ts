import { useAuthContext } from "../../Context"
import { IThreadsModeration } from "./Threads.types"

const useThreadsModeration = (): IThreadsModeration | null => {
  const user = useAuthContext()

  if (!user || !user.isModerator) return null

  return {
    closeThreads: () => console.log("CLOSE THREADS"),
    openThreads: () => console.log("CLOSE THREADS"),
    moveThreads: () => console.log("CLOSE THREADS"),
    deleteThreads: () => console.log("CLOSE THREADS"),
  }
}

export default useThreadsModeration
