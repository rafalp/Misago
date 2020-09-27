import { MockedProvider } from "@apollo/react-testing"
import React from "react"
import { AuthContext, ModalConsumer, ModalProvider } from "../../Context"
import {
  SettingsContextFactory,
  categories,
  userFactory,
} from "../../UI/Storybook"
import PostThread from "./PostThread"
import PostThreadAuthRequiredError from "./PostThreadAuthRequiredError"
import PostThreadPermissionDeniedError from "./PostThreadPermissionDeniedError"
import { CATEGORIES_QUERY } from "./useCategoriesQuery"

export default {
  title: "Route/Post Thread",
}

const graphqlMocks = [
  {
    request: {
      query: CATEGORIES_QUERY,
    },
    result: {
      data: {
        categories: categories.map((category) => {
          return Object.assign({}, category, {
            __typename: "category",
            children: category.children.map((child) => {
              return Object.assign({}, child, {
                __typename: "category",
              })
            }),
          })
        }),
      },
    },
  },
]

export const Form = () => (
  <ModalProvider>
    <SettingsContextFactory>
      <AuthContext.Provider value={userFactory()}>
        <MockedProvider mocks={graphqlMocks}>
          <PostThread />
        </MockedProvider>
        <ModalConsumer />
      </AuthContext.Provider>
    </SettingsContextFactory>
  </ModalProvider>
)

export const ModeratorForm = () => (
  <ModalProvider>
    <SettingsContextFactory>
      <AuthContext.Provider value={userFactory({ isModerator: true })}>
        <MockedProvider mocks={graphqlMocks}>
          <PostThread />
        </MockedProvider>
        <ModalConsumer />
      </AuthContext.Provider>
    </SettingsContextFactory>
  </ModalProvider>
)

export const AuthRequiredError = () => (
  <SettingsContextFactory>
    <PostThreadAuthRequiredError />
  </SettingsContextFactory>
)

export const PermissionDeniedError = () => (
  <SettingsContextFactory>
    <PostThreadPermissionDeniedError />
  </SettingsContextFactory>
)
