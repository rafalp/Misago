import { useApolloClient } from "@apollo/react-hooks"
import { getItem, removeItem, setItem } from "./localStorage"

const AUTH_TOKEN = "token"

const getAuthToken = () => getItem(AUTH_TOKEN)

const useAuth = () => {
  const client = useApolloClient()

  return {
    login: (token: string, user: { id: string; name: string }) => {
      client.resetStore()
      setItem(AUTH_TOKEN, token)
    },
    logout: () => {
      client.resetStore()
      removeItem(AUTH_TOKEN)
    },
  }
}

export { useAuth, getAuthToken }
