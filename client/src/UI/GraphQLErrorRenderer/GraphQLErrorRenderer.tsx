import { ApolloError } from "apollo-client"
import React from "react"
import getNetworkErrorCode from "../getNetworkErrorCode"

interface IGraphQLErrorRendererProps {
  error: ApolloError
  networkError: React.ReactElement
  queryError: React.ReactElement
}

const GraphQLErrorRenderer: React.FC<IGraphQLErrorRendererProps> = ({
  error,
  networkError,
  queryError,
}) => {
  console.log(error)
  const code = getNetworkErrorCode(error)

  if (error.networkError && code !== 400) {
    return networkError
  }

  return queryError
}

export default GraphQLErrorRenderer
