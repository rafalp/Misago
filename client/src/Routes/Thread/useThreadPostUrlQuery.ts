import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"

const THREAD_POST_URL_QUERY = gql`
  query ThreadPostUrl($id: ID!, $postId: ID!) {
    thread(id: $id) {
      id
      postUrl(id: $postId)
    }
  }
`

interface ThreadPostUrlVariables {
  id: string
  postId: string
}

interface ThreadPostUrlData {
  thread: {
    postUrl: string | null
  } | null
}

const useThreadPostUrlQuery = (variables: ThreadPostUrlVariables) => {
  return useQuery<ThreadPostUrlData, ThreadPostUrlVariables>(
    THREAD_POST_URL_QUERY,
    {
      variables,
      fetchPolicy: "network-only",
    }
  )
}

export default useThreadPostUrlQuery
