import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { CategoryChoice } from "./PostThread.types"

export const CATEGORIES_QUERY = gql`
  query CategoryChoices {
    categories {
      id
      name
      icon
      color
      isClosed
      extra
      children {
        id
        name
        icon
        color
        isClosed
        extra
      }
    }
  }
`

interface CategoriesQueryData {
  categories: Array<CategoryChoice>
}

const useCategoriesQuery = () => {
  return useQuery<CategoriesQueryData>(CATEGORIES_QUERY)
}

export default useCategoriesQuery
