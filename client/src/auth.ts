import { useApolloClient } from "@apollo/react-hooks"
import { getItem, removeItem, setItem } from "./localStorage"

const AUTH_TOKEN = "token"
const AUTH_USER = "user"

const getAuthToken = () => getItem(AUTH_TOKEN)

interface AuthOptions {
  token: string
  user: { id: string; name: string }
  preserveStore?: boolean
}

const useAuth = () => {
  const client = useApolloClient()

  return {
    login: (auth: AuthOptions) => {
      setItem(AUTH_TOKEN, auth.token)
      setItem(
        AUTH_USER,
        JSON.stringify({ id: auth.user.id, name: auth.user.name })
      )
      if (!auth.preserveStore) client.resetStore()
    },
    logout: () => {
      removeItem(AUTH_TOKEN)
      removeItem(AUTH_USER)
      client.resetStore()
    },
  }
}

export { AUTH_TOKEN, AUTH_USER, useAuth, getAuthToken }
