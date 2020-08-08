import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../../../types"
import { IPost } from "../Thread.types"

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
        body
        edits
      }
    }
  }
`

interface IEditPostMutationData {
  editPost: {
    errors: Array<IMutationError> | null
    post: {
      id: string
      body: { text: string }
      edits: number
    } | null
  }
}

interface IEditPostMutationVariables {
  input: {
    post: string
    body: string
  }
}

const useEditPostMutation = (post: IPost) => {
  const [mutation, { data, error, loading }] = useMutation<
    IEditPostMutationData,
    IEditPostMutationVariables
  >(EDIT_POST)

  return {
    data,
    error,
    loading,
    editPost: (body: string) => {
      return mutation({
        variables: {
          input: { body, post: post.id },
        },
      })
    },
  }
}

export default useEditPostMutation
