import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { RichText } from "../../../types"

export const POST_MARKUP_QUERY = gql`
  query PostMarkup($id: ID!) {
    post(id: $id) {
      id
      markup
      richText
    }
  }
`

interface PostMarkupVariables {
  id: string
}

interface PostMarkupData {
  post: {
    id: string
    markup: string
    richText: RichText
  } | null
}

const usePostMarkupQuery = (variables: PostMarkupVariables) => {
  return useQuery<PostMarkupData, PostMarkupVariables>(POST_MARKUP_QUERY, {
    variables,
    fetchPolicy: "network-only",
  })
}

export default usePostMarkupQuery
