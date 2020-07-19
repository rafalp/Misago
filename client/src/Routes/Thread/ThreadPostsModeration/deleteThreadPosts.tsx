import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { getSelectionErrors } from "../../../UI"
import { ICategory, IMutationError } from "../../../types"
import { IPost, IThread } from "../Thread.types"
import { THREAD_QUERY, IThreadData } from "../useThreadQuery"

const POST_NOT_EXISTS = "value_error.post.not_exists"

const DELETE_THREAD_POSTS = gql`
  mutation DeleteThreadReplies($input: BulkDeletePostsInput!) {
    deleteThreadReplies(input: $input) {
      errors {
        message
        location
        type
      }
      deleted
    }
  }
`

interface IDeleteThreadPostsMutationData {
  deleteThreadReplies: {
    errors: Array<IMutationError> | null
    deleted: boolean
  }
}

interface IDeleteThreadPostsMutationVariables {
  input: {
    thread: string
    replies: Array<string>
  }
}

const useDeleteThreadPostsMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IDeleteThreadPostsMutationData,
    IDeleteThreadPostsMutationVariables
  >(DELETE_THREAD_POSTS)

  return {
    data,
    error,
    loading,
    deletePosts: (
      thread: IThread,
      posts: Array<IPost>,
      page?: number | null
    ) => {
      const deletedPosts = posts.map((posts) => posts.id)

      return mutation({
        variables: {
          input: { thread: thread.id, replies: deletedPosts },
        },
        update: (cache, { data }) => {
          if (!data || !data.deleteThreadReplies) return

          const errors = getSelectionErrors<IPost>(
            "replies",
            posts,
            data.deleteThreadReplies.errors || []
          )

          const queryID = page
            ? {
                query: THREAD_QUERY,
                variables: { page, thread: thread.id },
              }
            : {
                query: THREAD_QUERY,
                variables: { thread: thread.id },
              }

          const query = cache.readQuery<IThreadData>(queryID)
          if (!query?.thread?.posts.page?.items.length) return null

          cache.writeQuery<IThreadData>({
            ...queryID,
            data: {
              ...query,
              thread: {
                ...query.thread,
                posts: {
                  ...query.thread.posts,
                  page: {
                    ...query.thread.posts.page,
                    items: query.thread.posts.page.items.filter((post) => {
                      if (
                        errors[post.id] &&
                        errors[post.id].type !== POST_NOT_EXISTS
                      ) {
                        return true
                      }

                      return deletedPosts.indexOf(post.id) < 0
                    }),
                  },
                },
              },
            },
          })
        },
      })
    },
  }
}

export default useDeleteThreadPostsMutation
