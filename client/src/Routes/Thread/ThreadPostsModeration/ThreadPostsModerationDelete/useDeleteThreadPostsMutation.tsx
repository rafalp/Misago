import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { getSelectionErrors } from "../../../../UI/useSelectionErrors"
import { MutationError } from "../../../../types"
import { IPost, Thread } from "../../Thread.types"
import { THREAD_QUERY, ThreadData } from "../../useThreadQuery"

const POST_NOT_EXISTS = "value_error.post.not_exists"

const DELETE_THREAD_POSTS = gql`
  mutation DeleteThreadPosts($input: BulkDeleteThreadPostsInput!) {
    deleteThreadPosts(input: $input) {
      errors {
        message
        location
        type
      }
      thread {
        id
        lastPostedAt
        replies
        lastPosterName
        lastPoster {
          id
          name
          slug
          extra
          avatars {
            size
            url
          }
        }
        posts {
          pagination {
            pages
          }
        }
      }
      deleted
    }
  }
`

interface IDeleteThreadPostsMutationData {
  deleteThreadPosts: {
    errors: Array<MutationError> | null
    deleted: Array<string>
  }
}

interface IDeleteThreadPostsMutationVariables {
  input: {
    thread: string
    posts: Array<string>
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
      thread: Thread,
      posts: Array<IPost>,
      page: number | undefined
    ) => {
      const deletedPosts = posts.map((posts) => posts.id)

      return mutation({
        variables: {
          input: { thread: thread.id, posts: deletedPosts },
        },
        update: (cache, { data }) => {
          if (!data || !data.deleteThreadPosts) return

          const errors = getSelectionErrors<IPost>(
            "posts",
            posts,
            data.deleteThreadPosts.errors || []
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

          const query = cache.readQuery<ThreadData>(queryID)
          if (!query?.thread?.posts.page?.items.length) return null

          cache.writeQuery<ThreadData>({
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

                      return (
                        data.deleteThreadPosts.deleted.indexOf(post.id) < 0
                      )
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
