import { useApolloClient } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { useCallback } from "react"
import { IAvatar } from "../types"

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

interface ISearchUsersQueryData {
  search: {
    users: Array<IUserSearchResult>
  }
}

export interface IUserSearchResult {
  name: string
  fullName: string | null
  avatar: IAvatar
}

interface ISearchUsersQueryVariables {
  query: string
}

const useSearchUsersQuery = () => {
  const { query } = useApolloClient()

  const searchUsers = useCallback(
    async (search: string) => {
      if (search.trim().length === 0) return []

      try {
        const result = await query<
          ISearchUsersQueryData,
          ISearchUsersQueryVariables
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
