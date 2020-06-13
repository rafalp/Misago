import { useAuthContext } from "./Context"

interface IThread {
  isClosed: boolean
  starter: { id: string } | null
  category: { id: string; isClosed: boolean }
}

export const useThreadACL = (thread?: IThread | null) => {
  const user = useAuthContext()

  if (!thread || !user) {
    return {
      edit: false,
      moderate: false,
    }
  }

  if (user.isModerator) {
    return {
      edit: true,
      moderate: true,
    }
  }

  const isClosed = thread.isClosed || thread.category.isClosed
  return {
    edit: user.id === thread.starter?.id && !isClosed,
    moderate: false,
  }
}
