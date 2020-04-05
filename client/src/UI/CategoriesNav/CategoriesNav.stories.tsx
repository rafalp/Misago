import React from "react"
import { CategoriesContext } from "../../Context"
import { Layout, LayoutSide } from "../Layout"
import { RootContainer, categories } from "../Storybook"
import CategoriesNav from "./CategoriesNav"

export default {
  title: "UI/CategoriesNav",
}

export const Default = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)

export const SelectedCategory = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "5", parent: null }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)

export const SelectedParent = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "6", parent: null }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)

export const SelectedFirstChild = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "7", parent: { id: "6" } }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)

export const SelectedChild = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "10", parent: { id: "6" } }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)

export const SelectedLastParent = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "13", parent: null }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)
export const SelectedLastChild = () => (
  <CategoriesContext.Provider value={categories}>
    <RootContainer padding>
      <Layout>
        <LayoutSide>
          <CategoriesNav active={{ id: "15", parent: {id: "13"} }} />
        </LayoutSide>
      </Layout>
    </RootContainer>
  </CategoriesContext.Provider>
)