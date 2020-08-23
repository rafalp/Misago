import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"

const THREAD_POST_URL_QUERY = gql`
  query ThreadPostUrl($id: ID!, $postId: ID!) {
    thread(id: $id) {
      postUrl(id: $postId)
    }
  }
`

interface IThreadPostUrlVariables {
  id: string
  postId: string
}

interface IThreadPostUrlData {
  thread: {
    postUrl: string | null
  } | null
}

const useThreadPostUrlQuery = (variables: IThreadPostUrlVariables) => {
  return useQuery<IThreadPostUrlData, IThreadPostUrlVariables>(
    THREAD_POST_URL_QUERY,
    {
      variables,
      fetchPolicy: "network-only",
    }
  )
}

export default useThreadPostUrlQuery
