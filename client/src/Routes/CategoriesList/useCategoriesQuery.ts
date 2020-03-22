import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"

const POLL_INTERVAL = 50 * 1000 // 50s

const CATEGORIES_QUERY = gql`
  query Categories {
    categories {
      id
      name
      slug
      color
      children {
        id
        name
        slug
        color
      }
    }
  }
`

interface ICategoriesData {
  categories: Array<Category>
}

interface Category {
  id: string
  name: string
  slug: string
  color: string
  children: Array<ChildCategory>
}

interface ChildCategory {
  id: string
  name: string
  slug: string
  color: string
}

const useCategoriesQuery = () => {
  return useQuery<ICategoriesData>(CATEGORIES_QUERY, {
    pollInterval: POLL_INTERVAL,
  })
}

export default useCategoriesQuery