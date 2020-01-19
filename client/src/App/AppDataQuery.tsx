import { useQuery } from "@apollo/react-hooks"
import { gql } from "apollo-boost"
import { ApolloError } from "apollo-client"
import React from "react"
import { ICategory, ISettings, IUser } from "../types"
import AppError from "./AppError"
import AppLoader from "./AppLoader"

const POLL_INTERVAL = 2 * 1000 // 50s

const INITIAL_DATA = gql`
  query InitialData {
    auth {
      id
      name
      avatars {
        size
        url
      }
    }
    categories {
      id
      name
      slug
      color
      children {
        id
        name
        slug
        color
      }
    }
    settings {
      forumName
      passwordMinLength
      passwordMaxLength
      usernameMinLength
      usernameMaxLength
    }
  }
`

interface IInitialData {
  auth: IUser | null
  categories: Array<ICategory>
  settings: ISettings | null
}

interface IAppDataChildrenProps {
  data: IInitialData
  error: ApolloError | undefined
  loading: boolean
}

interface IAppDataProps {
  children: (props: IAppDataChildrenProps) => React.ReactElement
}

const defaultData = {
  auth: null,
  categories: [],
  settings: null,
}

const AppDataQuery: React.FC<IAppDataProps> = ({ children }) => {
  const { data, error, loading } = useQuery<IInitialData>(INITIAL_DATA, {
    pollInterval: POLL_INTERVAL,
  })

  if (!data) {
    if (loading) return <AppLoader />
    if (error) return <AppError />
  }

  return children({ error, loading, data: data || defaultData })
}

export default AppDataQuery
