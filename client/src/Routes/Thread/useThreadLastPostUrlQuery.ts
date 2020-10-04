import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"

const THREAD_LAST_POST_URL_QUERY = gql`
  query ThreadLastPostUrl($id: ID!) {
    thread(id: $id) {
      id
      lastPostUrl
    }
  }
`

interface IThreadLastPostUrlVariables {
  id: string
}

interface IThreadLastPostUrlData {
  thread: {
    lastPostUrl: string | null
  } | null
}

const useThreadLastPostUrlQuery = (variables: IThreadLastPostUrlVariables) => {
  return useQuery<IThreadLastPostUrlData, IThreadLastPostUrlVariables>(
    THREAD_LAST_POST_URL_QUERY,
    {
      variables,
      fetchPolicy: "network-only",
    }
  )
}

export default useThreadLastPostUrlQuery
