import { ApolloError } from "apollo-client"
import React from "react"
import { ButtonPrimary } from "../Button"
import { RootContainer } from "../Storybook"
import BaseError from "./Error"
import GraphQLError from "./GraphQLError"
import NotFoundError from "./NotFoundError"

export default {
  title: "UI/Error",
}

export const Default = () => (
  <RootContainer>
    <BaseError className="test" />
  </RootContainer>
)

export const NotFound = () => (
  <RootContainer>
    <NotFoundError className="test" />
  </RootContainer>
)

export const QueryError = () => (
  <RootContainer>
    <GraphQLError className="test" error={new ApolloError({})} />
  </RootContainer>
)

export const NetworkError = () => (
  <RootContainer>
    <GraphQLError
      className="test"
      error={new ApolloError({ networkError: new Error() })}
    />
  </RootContainer>
)

export const WithAction = () => (
  <RootContainer>
    <BaseError
      className="test"
      action={
        <ButtonPrimary text="Do something" responsive onClick={() => {}} />
      }
    />
  </RootContainer>
)
