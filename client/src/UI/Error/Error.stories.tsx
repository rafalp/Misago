import { ApolloError } from "apollo-client"
import React from "react"
import { RootContainer } from "../Storybook"
import BaseError from "./Error"
import GraphQLError from "./GraphQLError"
import NotFoundError from "./NotFoundError"

export default {
  title: "UI/Error",
}

export const Default = () => (
  <RootContainer padding>
    <BaseError className="test" />
  </RootContainer>
)

export const NotFound = () => (
  <RootContainer padding>
    <NotFoundError className="test" />
  </RootContainer>
)

export const QueryError = () => (
  <RootContainer padding>
    <GraphQLError className="test" error={new ApolloError({})} />
  </RootContainer>
)

export const NetworkError = () => (
  <RootContainer padding>
    <GraphQLError
      className="test"
      error={new ApolloError({ networkError: new Error() })}
    />
  </RootContainer>
)
