import { useQuery } from "@apollo/react-hooks"
import { ApolloError } from "apollo-client"
import gql from "graphql-tag"
import React from "react"
import { RouteGraphQLError, RouteNotFound } from "../../UI/RouteError"
import RouteLoader from "../../UI/RouteLoader"

const POLL_INTERVAL = 50 * 1000 // 50s

const USER_QUERY = gql`
  query UserProfile($id: ID!) {
    user(id: $id) {
      id
      slug
      name
    }
  }
`

interface UserProfile {
  id: string
  slug: string
  name: string
}

interface UserQueryData {
  user: UserProfile | null
}

interface UserQueryProps {
  id: string
  children: (props: UserQueryChildrenProps) => React.ReactElement
}

interface UserQueryChildrenProps {
  data: { user: UserProfile }
  error: ApolloError | undefined
  loading: boolean
}

const UserQuery: React.FC<UserQueryProps> = ({ children, id }) => {
  const { data, error, loading } = useQuery<UserQueryData>(USER_QUERY, {
    pollInterval: POLL_INTERVAL,
    variables: { id },
  })

  if (!data) {
    if (loading) return <RouteLoader />
    if (error) return <RouteGraphQLError error={error} />
  }

  if (!data || !data.user) {
    return <RouteNotFound />
  }

  return children({ error, loading, data: { user: data.user } })
}

export default UserQuery
