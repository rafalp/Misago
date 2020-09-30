import React from "react"
import { CategoriesContext } from "../../Context"
import { Layout, LayoutSide } from "../Layout"
import {
  RootContainer,
  SettingsContextFactory,
  categories,
} from "../Storybook"
import CategoriesNav from "./CategoriesNav"

export default {
  title: "UI/CategoriesNav",
}

export const Default = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const SelectedCategory = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "5" }, parent: { id: "5" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const SelectedParent = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "6" }, parent: { id: "6" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const SelectedFirstChild = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "7" }, parent: { id: "6" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const SelectedChild = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "10" }, parent: { id: "6" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)

export const SelectedLastParent = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "13" }, parent: { id: "13" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)
export const SelectedLastChild = () => (
  <SettingsContextFactory>
    <CategoriesContext.Provider value={categories}>
      <RootContainer>
        <Layout>
          <LayoutSide>
            <CategoriesNav
              active={{ category: { id: "15" }, parent: { id: "13" } }}
            />
          </LayoutSide>
        </Layout>
      </RootContainer>
    </CategoriesContext.Provider>
  </SettingsContextFactory>
)
