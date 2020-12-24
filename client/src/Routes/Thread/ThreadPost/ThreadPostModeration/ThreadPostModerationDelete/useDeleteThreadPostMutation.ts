import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../../../../../types"
import { IPost } from "../../../Thread.types"
import { THREAD_QUERY, IThreadData } from "../../../useThreadQuery"

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

interface IDeleteThreadPostMutationData {
  deleteThreadPost: {
    errors: Array<MutationError> | null
    deleted: Array<string>
  }
}

interface IDeleteThreadPostMutationVariables {
  input: {
    thread: string
    post: string
  }
}

const useDeleteThreadPostMutation = () => {
  const [mutation, { data, error, loading }] = useMutation<
    IDeleteThreadPostMutationData,
    IDeleteThreadPostMutationVariables
  >(DELETE_THREAD_POST)

  return {
    data,
    error,
    loading,
    deletePost: (threadId: string, post: IPost, page: number | undefined) => {
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
