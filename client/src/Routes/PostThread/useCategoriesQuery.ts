import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { ICategoryChoice } from "./PostThread.types"

const CATEGORIES_QUERY = gql`
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

interface ICategoriesQueryData {
  categories: Array<ICategoryChoice>
}

const useCategoriesQuery = () => {
  return useQuery<ICategoriesQueryData>(CATEGORIES_QUERY)
}

export default useCategoriesQuery
