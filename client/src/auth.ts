import { useApolloClient } from "@apollo/react-hooks"
import { getItem, removeItem, setItem } from "./localStorage"

const AUTH_TOKEN = "token"
const AUTH_USER = "user"

const getAuthToken = () => getItem(AUTH_TOKEN)

const useAuth = () => {
  const client = useApolloClient()

  return {
    login: (token: string, user: { id: string; name: string }) => {
      setItem(AUTH_TOKEN, token)
      setItem(AUTH_USER, JSON.stringify({ id: user.id, name: user.name }))
      client.resetStore()
    },
    logout: () => {
      removeItem(AUTH_TOKEN)
      removeItem(AUTH_USER)
      client.resetStore()
    },
  }
}

export { AUTH_TOKEN, AUTH_USER, useAuth, getAuthToken }
