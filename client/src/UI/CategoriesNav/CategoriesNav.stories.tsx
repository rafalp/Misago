import React from "react"
import { CategoriesContext } from "../../Context"
import { Layout, LayoutSide } from "../Layout"
import { RootContainer } from "../Storybook"
import CategoriesNav from "./CategoriesNav"

export default {
  title: "UI/CategoriesNav",
}

const categories = [
  {
    id: "1",
    name: "EVE Information Portal",
    slug: "category",
    color: "#ff5630",
    children: [
      {
        id: "2",
        name: "Dev Blogs",
        slug: "category",
        color: "#36b37e",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "3",
        name: "Announcements",
        slug: "category",
        color: "#ffab00",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "4",
        name: "Community Fittings",
        slug: "category",
        color: "#00b8d9",
        children: [],
        depth: 1,
        parent: null,
      },
    ],
    depth: 0,
    parent: null,
  },
  {
    id: "5",
    name: "New Citizens Q&A",
    slug: "category",
    color: "#6554c0",
    children: [],
    depth: 0,
    parent: null,
  },
  {
    id: "6",
    name: "Communications Center",
    slug: "category",
    color: "#ff5630",
    children: [
      {
        id: "7",
        name: "General discussion",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "8",
        name: "Crime & Punishment",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "9",
        name: "Out Of Pod Experience",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "10",
        name: "My EVE",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "11",
        name: "Skill Discussion",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
    ],
    depth: 0,
    parent: null,
  },
  {
    id: "12",
    name: "Fiction Portal",
    slug: "category",
    color: "#ff5630",
    children: [],
    depth: 0,
    parent: null,
  },
  {
    id: "13",
    name: "Events",
    slug: "category",
    color: "#ff5630",
    children: [
      {
        id: "14",
        name: "In Game Events",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "15",
        name: "Out of Game Events",
        slug: "category",
        color: "#ff5630",
        children: [],
        depth: 1,
        parent: null,
      },
    ],
    depth: 0,
    parent: null,
  },
]

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