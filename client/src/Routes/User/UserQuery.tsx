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

interface IUserProfile {
  id: string
  slug: string
  name: string
}

interface IUserQueryData {
  user: IUserProfile | null
}

interface IUserQueryProps {
  id: string
  children: (props: IUserQueryChildrenProps) => React.ReactElement
}

interface IUserQueryChildrenProps {
  data: { user: IUserProfile }
  error: ApolloError | undefined
  loading: boolean
}

const UserQuery: React.FC<IUserQueryProps> = ({ children, id }) => {
  const { data, error, loading } = useQuery<IUserQueryData>(USER_QUERY, {
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
