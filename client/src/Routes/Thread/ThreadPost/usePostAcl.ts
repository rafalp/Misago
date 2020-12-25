import { useAuthContext } from "../../../Context"

interface Post {
  poster: {
    id: string
  } | null
}

const usePostAcl = (post: Post, isClosed?: boolean) => {
  const user = useAuthContext()

  if (user) {
    if (user.isModerator) return { edit: true }
    if (user && post.poster && !isClosed) {
      return { edit: user.id === post.poster.id }
    }
  }

  return { edit: false }
}

export default usePostAcl
