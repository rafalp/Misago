import { useMutation } from "@apollo/react-hooks"
import gql from "graphql-tag"
import { IMutationError } from "../types"

const SETUP_SITE = gql`
  mutation SetupSite($input: SetupSiteInput!) {
    setupSite(input: $input) {
      errors {
        message
        location
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

interface SetupSiteMutationData {
  setupSite: {
    errors: Array<IMutationError> | null
    user: { id: string; name: string } | null
    token: string | null
  }
}

interface SetupSiteMutationVariables {
  input: {
    forumName: string
    forumIndexThreads: boolean
    name: string
    email: string
    password: string
  }
}

const useSetupSiteMutation = () => {
  return useMutation<SetupSiteMutationData, SetupSiteMutationVariables>(
    SETUP_SITE
  )
}

export default useSetupSiteMutation
