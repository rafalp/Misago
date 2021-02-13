import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { MutationError } from "../types"

const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
      errors {
        location
        message
        type
      }
      user {
        id
        name
      }
      token
    }
  }
`

interface LoginData {
  login: {
    errors: Array<MutationError> | null
    user: {
      id: string
      name: string
    } | null
    token: string | null
  }
}

interface LoginValues {
  username: string
  password: string
}

const useLoginMutation = () => {
  return useMutation<LoginData, LoginValues>(LOGIN, {
    errorPolicy: "all",
  })
}

export default useLoginMutation
