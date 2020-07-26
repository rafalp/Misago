import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { getSelectionErrors } from "../../../UI"
import { IMutationError } from "../../../types"
import { IPost, IThread } from "../Thread.types"
import { THREAD_QUERY, IThreadData } from "../useThreadQuery"

const POST_NOT_EXISTS = "value_error.post.not_exists"

const DELETE_THREAD_REPLIES = gql`
  mutation DeleteThreadReplies($input: BulkDeleteThreadRepliesInput!) {
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

interface IDeleteThreadRepliesMutationData {
  deleteThreadReplies: {
    errors: Array<IMutationError> | null
    deleted: boolean
  }
}

interface IDeleteThreadRepliesMutationVariables {
  input: {
    thread: string
    replies: Array<string>
  }
}

const useDeleteThreadRepliesMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IDeleteThreadRepliesMutationData,
    IDeleteThreadRepliesMutationVariables
  >(DELETE_THREAD_REPLIES)

  return {
    data,
    error,
    loading,
    deleteReplies: (
      thread: IThread,
      posts: Array<IPost>,
      page: number | undefined
    ) => {
      const deletedReplies = posts.map((posts) => posts.id)

      return mutation({
        variables: {
          input: { thread: thread.id, replies: deletedReplies },
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
                variables: { page, id: thread.id },
              }
            : {
                query: THREAD_QUERY,
                variables: { id: thread.id },
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

                      return deletedReplies.indexOf(post.id) < 0
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

export default useDeleteThreadRepliesMutation
