import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../types"

const POST_REPLY = gql`
  mutation PostReply($input: PostReplyInput!) {
    postReply(input: $input) {
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
      post {
        id
      }
    }
  }
`

interface IPostReplyMutationData {
  postReply: {
    errors: Array<MutationError> | null
    thread: {
      id: string
      slug: string
    } | null
    post: {
      id: string
    } | null
  }
}

interface IPostReplyMutationValues {
  input: {
    thread: string
    markup: string
  }
}

const usePostReplyMutation = () => {
  return useMutation<IPostReplyMutationData, IPostReplyMutationValues>(
    POST_REPLY
  )
}

export default usePostReplyMutation
