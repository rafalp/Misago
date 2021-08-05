import { useQuery } from "@apollo/react-hooks"
import { ApolloError } from "apollo-client"
import gql from "graphql-tag"
import React from "react"
import { AuthUser, Category, ForumStats, Settings } from "../types"
import AppError from "./AppError"
import AppLoader from "./AppLoader"

const POLL_INTERVAL = 5 * 1000 // 50s

const INITIAL_DATA_QUERY = gql`
  fragment CategoryBanner on CategoryBanner {
    align
    background
    height
    url
  }

  fragment CategoryFields on Category {
    id
    name
    slug
    color
    icon
    banner {
      full {
        ...CategoryBanner
      }
      half {
        ...CategoryBanner
      }
    }
    threads
    posts
    isClosed
  }

  query InitialData {
    auth {
      id
      name
      slug
      avatars {
        size
        url
      }
      isAdmin
      isModerator
    }
    categories {
      ...CategoryFields
      children {
        ...CategoryFields
      }
    }
    settings {
      bulkActionLimit
      enableSiteWizard
      forumIndexHeader
      forumIndexThreads
      forumIndexTitle
      forumName
      passwordMinLength
      passwordMaxLength
      postMinLength
      threadTitleMinLength
      threadTitleMaxLength
      usernameMinLength
      usernameMaxLength
    }
    forumStats {
      threads
      posts
      users
    }
  }
`

interface InitialData {
  auth: AuthUser | null
  categories: Array<Category>
  settings: Settings | null
  forumStats: ForumStats | null
}

interface AppDataProps {
  children: (props: AppDataChildrenProps) => React.ReactElement
}

interface AppDataChildrenProps {
  data: InitialData
  error: ApolloError | undefined
  loading: boolean
}

const defaultData = {
  auth: null,
  categories: [],
  settings: null,
  forumStats: null,
}

const AppDataQuery: React.FC<AppDataProps> = ({ children }) => {
  const { data, error, loading, stopPolling } = useQuery<InitialData>(
    INITIAL_DATA_QUERY,
    {
      pollInterval: POLL_INTERVAL,
    }
  )

  const enableSiteWizard = React.useMemo(() => {
    return data?.settings?.enableSiteWizard || false
  }, [data])

  React.useEffect(() => {
    if (enableSiteWizard) {
      stopPolling() // Prevent updated settings kicking users off the wizard
    }
  }, [enableSiteWizard, stopPolling])

  if (!data) {
    if (loading) return <AppLoader />
    if (error) return <AppError />
  }

  return children({ error, loading, data: data || defaultData })
}

export default AppDataQuery
