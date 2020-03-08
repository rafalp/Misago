import { ApolloError } from "apollo-client"

const getNetworkErrorCode = (error: ApolloError): number => {
  if (!error.networkError) return 0;
  if (!("statusCode" in error.networkError)) return 0;
  return error.networkError["statusCode"]
}

export default getNetworkErrorCode 