import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError, RichText } from "../../../types"

const EDIT_POST = gql`
  mutation EditPost($input: EditPostInput!) {
    editPost(input: $input) {
      errors {
        message
        location
        type
      }
      post {
        id
        richText
        edits
      }
    }
  }
`

interface EditPostMutationData {
  editPost: {
    errors: Array<MutationError> | null
    post: {
      id: string
      richText: RichText
      edits: number
    } | null
  }
}

interface EditPostMutationVariables {
  input: {
    post: string
    markup: string
  }
}

const useEditPostMutation = (post: { id: string }) => {
  const [mutation, { data, error, loading }] = useMutation<
    EditPostMutationData,
    EditPostMutationVariables
  >(EDIT_POST)

  return {
    data,
    error,
    loading,
    editPost: (markup: string) => {
      return mutation({
        variables: {
          input: { markup, post: post.id },
        },
      })
    },
  }
}

export default useEditPostMutation
