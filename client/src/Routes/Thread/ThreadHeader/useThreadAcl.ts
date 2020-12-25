import { useAuthContext } from "../../../Context"

interface Thread {
  isClosed: boolean
  starter: { id: string } | null
  category: { id: string; isClosed: boolean }
}

const useThreadAcl = (thread?: Thread | null) => {
  const user = useAuthContext()

  if (!thread || !user) {
    return {
      edit: false,
    }
  }

  if (user.isModerator) {
    return {
      edit: true,
    }
  }

  const isClosed = thread.isClosed || thread.category.isClosed
  return {
    edit: user.id === thread.starter?.id && !isClosed,
  }
}

export default useThreadAcl
