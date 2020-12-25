import { useParams } from "react-router-dom"

interface ThreadRouteParams {
  id: string
  slug: string
  page?: string
}

const useThreadParams = () => {
  const params = useParams<ThreadRouteParams>()
  const { id, slug } = params
  const page = params.page ? Number(params.page) : undefined
  return { id, slug, page }
}

export default useThreadParams
