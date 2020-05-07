import { ApolloError } from "apollo-client"
import React from "react"
import { Error as BaseError, GraphQLError, NotFoundError } from "../Error"
import RouteContainer from "../RouteContainer"
import { RouteLoaderSpinner } from "../RouteLoader"
import { Placeholder, RootContainer } from "../Storybook"
import Layout from "./Layout"
import LayoutMain from "./LayoutMain"
import LayoutSide from "./LayoutSide"

export default {
  title: "UI/Layout",
}

export const TwoColumn = () => (
  <RootContainer padding>
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <Placeholder text="SIDE NAV" />
        </LayoutSide>
        <LayoutMain>
          <Placeholder text="MAIN CONTENT" />
        </LayoutMain>
      </Layout>
    </RouteContainer>
  </RootContainer>
)

export const MainLoading = () => (
  <RootContainer padding>
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <Placeholder text="SIDE NAV" />
        </LayoutSide>
        <LayoutMain>
          <RouteLoaderSpinner />
        </LayoutMain>
      </Layout>
    </RouteContainer>
  </RootContainer>
)

export const MainError = () => (
  <RootContainer padding>
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <Placeholder text="SIDE NAV" />
        </LayoutSide>
        <LayoutMain>
          <BaseError className="route" />
        </LayoutMain>
      </Layout>
    </RouteContainer>
  </RootContainer>
)

export const MainNotFound = () => (
  <RootContainer padding>
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <Placeholder text="SIDE NAV" />
        </LayoutSide>
        <LayoutMain>
          <NotFoundError className="route" />
        </LayoutMain>
      </Layout>
    </RouteContainer>
  </RootContainer>
)

export const MainNetworkError = () => (
  <RootContainer padding>
    <RouteContainer>
      <Layout>
        <LayoutSide>
          <Placeholder text="SIDE NAV" />
        </LayoutSide>
        <LayoutMain>
          <GraphQLError
            className="route"
            error={new ApolloError({ networkError: new Error() })}
          />
        </LayoutMain>
      </Layout>
    </RouteContainer>
  </RootContainer>
)
