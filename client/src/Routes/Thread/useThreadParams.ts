import { useParams } from "react-router-dom"

interface IThreadRouteParams {
  id: string
  slug: string
  page?: string
}

const useThreadParams = () => {
  const params = useParams<IThreadRouteParams>()
  const { id, slug } = params
  const page = params.page ? Number(params.page) : undefined
  return { id, slug, page }
}

export default useThreadParams
