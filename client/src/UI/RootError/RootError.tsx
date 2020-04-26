import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { ApolloError } from "apollo-client"
import { IMutationError } from "../../types"
import getNetworkErrorCode from "../getNetworkErrorCode"

interface IRootError {
  message: React.ReactNode
  type: string
}

interface IRootErrorProps {
  children: (error: IRootError) => React.ReactNode
  dataErrors?: Array<IMutationError> | null
  graphqlError?: ApolloError | null
  plainError?: string | null
  locations?: Array<string> | null
  messages?: {
    [type: string]: React.ReactNode
  }
}

const RootError: React.FC<IRootErrorProps> = ({
  children,
  dataErrors,
  graphqlError,
  plainError,
  locations,
  messages,
}) => (
  <I18n>
    {({ i18n }) => {
      if (plainError && messages && messages[plainError]) {
        return children({ type: plainError, message: messages[plainError] })
      }

      const errors: Array<IMutationError> = []
      if (graphqlError) {
        const code = getNetworkErrorCode(graphqlError)
        if (code === 400 || !graphqlError.networkError) {
          errors.push({
            location: ["__root__"],
            type: "client_error.graphql",
            message: i18n._(
              t("client_error.graphql")`Unexpected error has occurred.`
            ),
          })
        } else if (graphqlError.networkError) {
          errors.push({
            location: ["__root__"],
            type: "client_error.network",
            message: i18n._(
              t("client_error.network")`Site server can't be reached.`
            ),
          })
        }
      }

      if (dataErrors) errors.push(...dataErrors)
      if (!errors.length) return null

      const finLocations: Array<string> = locations || ["__root__"]
      const finMessages: { [type: string]: React.ReactNode } = messages || {}

      for (const location of finLocations) {
        for (const error of errors) {
          const errorLocation = error.location.join(".")
          if (errorLocation === location) {
            const { type, message } = error
            return children({ type, message: finMessages[type] || message })
          }
        }
      }

      return null
    }}
  </I18n>
)

export default RootError
