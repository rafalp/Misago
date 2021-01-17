import { useAuthContext } from "../../../Context"

interface IPost {
  poster: {
    id: string
  } | null
}

const usePostAcl = (post: IPost, isClosed?: boolean) => {
  const acl = {
    edit: false,
    reply: !isClosed,
  }

  const user = useAuthContext()

  if (!user) return acl
  if (user.isModerator) return { edit: true, reply: true }

  if (user && post.poster && !isClosed) {
    acl.edit = user.id === post.poster.id
  }

  return acl
}

export default usePostAcl
