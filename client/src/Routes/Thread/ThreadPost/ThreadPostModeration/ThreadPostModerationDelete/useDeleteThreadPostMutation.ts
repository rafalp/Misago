import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../../../types"
import { Post } from "../../../Thread.types"
import { THREAD_QUERY, ThreadData } from "../../../useThreadQuery"

const DELETE_THREAD_POST = gql`
  mutation DeleteThreadPost($input: DeleteThreadPostInput!) {
    deleteThreadPost(input: $input) {
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

interface DeleteThreadPostMutationData {
  deleteThreadPost: {
    errors: Array<MutationError> | null
    deleted: Array<string>
  }
}

interface DeleteThreadPostMutationVariables {
  input: {
    thread: string
    post: string
  }
}

const useDeleteThreadPostMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    DeleteThreadPostMutationData,
    DeleteThreadPostMutationVariables
  >(DELETE_THREAD_POST)

  return {
    data,
    error,
    loading,
    deletePost: (threadId: string, post: Post, page: number | undefined) => {
      return mutation({
        variables: {
          input: { thread: threadId, post: post.id },
        },
        update: (cache, { data }) => {
          if (!data || !data.deleteThreadPost) return

          const queryID = page
            ? {
                query: THREAD_QUERY,
                variables: { page, id: threadId },
              }
            : {
                query: THREAD_QUERY,
                variables: { id: threadId },
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
                      return data.deleteThreadPost.deleted.indexOf(post.id) < 0
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

export default useDeleteThreadPostMutation
