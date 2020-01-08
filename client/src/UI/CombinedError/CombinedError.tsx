import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { ApolloError } from "apollo-client"
import { IMutationError } from "../../types"

interface ICombinedError {
  message: React.ReactNode
  type: string
}

interface ICombinedErrorProps {
  children: (error: ICombinedError) => React.ReactElement
  clientError?: ApolloError | null
  graphqlErrors?: Array<IMutationError> | null
  locations?: Array<string> | null
  messages?: {
    [type: string]: React.ReactNode
  }
}

const CombinedError: React.FC<ICombinedErrorProps> = ({
  children,
  clientError,
  graphqlErrors,
  locations,
  messages,
}) => (
  <I18n>
    {({ i18n }) => {
      const errors: Array<IMutationError> = []
      if (clientError) {
        console.log()
        if (clientError.networkError) {
          errors.push({
            location: ["__root__"],
            type: "client_error.network",
            message: i18n._(t("client_error.network")`Site server can't be reached.`),
          })
        } else {
          errors.push({
            location: ["__root__"],
            type: "client_error.graphql",
            message: i18n._(t("client_error.graphql")`Unexpected error has occurred.`),
          })
        }
      }

      if (graphqlErrors) errors.push(...graphqlErrors)
      if (!errors.length) return null

      const finLocations: Array<string> = locations || ["__root__"]
      const finMessages: { [type: string]: React.ReactNode } = messages || {}

      for (const location of finLocations) {
        for (const error of errors) {
          const errorLocation = error.location.join(".")
          if (errorLocation === location) {
            const { type, message } = error
            return children({ type, message: finMessages[type] || message})
          }
        }
      }

      return null
    }}
  </I18n>
)

export default CombinedError
