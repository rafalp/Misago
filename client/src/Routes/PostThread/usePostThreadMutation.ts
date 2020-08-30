import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../types"

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

interface IPostThreadMutationData {
  postThread: {
    errors: Array<IMutationError> | null
    thread: {
      id: string
      title: string
      slug: string
    } | null
  }
}

interface IPostThreadMutationValues {
  input: {
    category: string
    title: string
    body: string
  }
}

const usePostThreadMutation = () => {
  return useMutation<IPostThreadMutationData, IPostThreadMutationValues>(
    POST_THREAD
  )
}

export default usePostThreadMutation
