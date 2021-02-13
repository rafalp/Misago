import { useAuthContext } from "../../Context"
import { CategoryAcl } from "./Threads.types"

interface Category {
  isClosed: boolean
}

const useCategoryAcl = (category?: Category | null): CategoryAcl => {
  const user = useAuthContext()

  // On root category always invite users to try start thread
  if (!category) return { start: true }

  // Mods can always start threads
  if (user && user.isModerator) return { start: true }

  // If category is open always invite user to try start thread
  return { start: !category.isClosed }
}

export default useCategoryAcl
