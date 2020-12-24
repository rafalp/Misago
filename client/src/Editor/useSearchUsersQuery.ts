import { useApolloClient } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { useCallback } from "react"
import { AvatarData } from "../types"

const SEARCH_USERS_QUERY = gql`
  query SearchUsersForMention($query: String!) {
    search(query: $query) {
      users {
        name
        fullName
        avatar(size: 32) {
          size
          url
        }
      }
    }
  }
`

interface SearchUsersQueryData {
  search: {
    users: Array<UserSearchResult>
  }
}

export interface UserSearchResult {
  name: string
  fullName: string | null
  avatar: AvatarData
}

interface SearchUsersQueryVariables {
  query: string
}

const useSearchUsersQuery = () => {
  const { query } = useApolloClient()

  const searchUsers = useCallback(
    async (search: string) => {
      if (search.trim().length === 0) return []

      try {
        const result = await query<
          SearchUsersQueryData,
          SearchUsersQueryVariables
        >({
          query: SEARCH_USERS_QUERY,
          variables: { query: search },
        })

        return result.data?.search.users || []
      } catch (error) {
        console.error(error)
        return []
      }
    },
    [query]
  )

  return searchUsers
}

export default useSearchUsersQuery
