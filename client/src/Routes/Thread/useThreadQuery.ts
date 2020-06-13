import { useQuery } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IThread } from "./Thread.types"

const THREAD_FRAGMENTS = `
  fragment ThreadPoster on User {
    id
    name
    slug
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

  query Thread($id: ID!) {
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
    }
  }
`

interface IThreadVariables {
  id: string
  page?: number
}

interface IThreadData {
  thread: IThread | null
}

export const useThreadQuery = (variables: IThreadVariables) => {
  return useQuery<IThreadData, IThreadVariables>(THREAD_QUERY, {
    variables,
    fetchPolicy: "network-only",
  })
}
