import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { Thread } from "./Thread.types"

const THREAD_FRAGMENTS = `
  fragment ThreadPoster on User {
    id
    name
    slug
    extra
    avatars {
      size
      url
    }
  }

  fragment ThreadCategory on Category {
    id
    name
    slug
    color
    icon
    isClosed
  }

  fragment ThreadCategoryBanner on CategoryBanner {
    align
    background
    height
    url
  }
`

export const THREAD_QUERY = gql`
  ${THREAD_FRAGMENTS}

  query Thread($id: ID!, $page: Int) {
    thread(id: $id) {
      id
      slug
      title
      startedAt
      lastPostedAt
      replies
      starterName
      lastPosterName
      isClosed
      starter {
        ...ThreadPoster
      }
      lastPoster {
        ...ThreadPoster
      }
      category {
        ...ThreadCategory
        banner {
          full {
            ...ThreadCategoryBanner
          }
          half {
            ...ThreadCategoryBanner
          }
        }
        parent {
          ...ThreadCategory
        }
      }
      posts {
        page(page: $page) {
          number
          items {
            id
            richText
            edits
            postedAt
            extra
            posterName
            poster {
              ...ThreadPoster
              extra
            }
          }
        }
        pagination {
          pages
        }
      }
    }
  }
`

interface ThreadVariables {
  id: string
  page?: number
}

export interface ThreadData {
  thread: Thread | null
}

export const useThreadQuery = (variables: ThreadVariables) => {
  return useQuery<ThreadData, ThreadVariables>(THREAD_QUERY, {
    variables,
    fetchPolicy: "network-only",
  })
}
