import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../types"

const POST_THREAD = gql`
  mutation PostThread($input: PostThreadInput!) {
    postThread(input: $input) {
      errors {
        location
        message
        type
      }
      thread {
        id
        title
        slug
      }
    }
  }
`

interface PostThreadMutationData {
  postThread: {
    errors: Array<MutationError> | null
    thread: {
      id: string
      title: string
      slug: string
    } | null
  }
}

interface PostThreadMutationValues {
  input: {
    category: string
    title: string
    markup: string
    isClosed?: boolean
  }
}

const usePostThreadMutation = () => {
  return useMutation<PostThreadMutationData, PostThreadMutationValues>(
    POST_THREAD
  )
}

export default usePostThreadMutation
