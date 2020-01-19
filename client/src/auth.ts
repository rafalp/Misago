import { useApolloClient } from "@apollo/react-hooks"
import { getItem, removeItem, setItem } from "./localStorage"

const AUTH_TOKEN = "token"

const getAuthToken = () => getItem(AUTH_TOKEN)

const useAuth = () => {
  const client = useApolloClient()

  return {
    login: (token: string, user: { id: string; name: string }) => {
      setItem(AUTH_TOKEN, token)
      client.resetStore()
    },
    logout: () => {
      removeItem(AUTH_TOKEN)
      client.resetStore()
    },
  }
}

export { useAuth, getAuthToken }
