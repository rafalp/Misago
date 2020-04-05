import React from "react"
import { CategoriesContext } from "../../Context"
import { Layout, LayoutSide } from "../Layout"
import { RootContainer } from "../Storybook"
import CategoriesNav from "./CategoriesNav"

export default {
  title: "UI/CategoriesNav",
}

const colors: Array<string> = [
  "#ff5630",
  "#36b37e",
  "#ffab00",
  "#00b8d9",
  "#6554c0",
  "#0065ff",
  "#ff7452",
  "#57d9a3",
  "#ffc400",
  "#00c7e6",
  "#8777d9",
  "#2684ff",
  "#de350b",
  "#00875a",
  "#ff991f",
  "#00a3bf",
  "#5243aa",
  "#0052cc",
]

const icons: Array<string> = [
  "fas fa-pencil-ruler",
  "fas fa-rocket",
  "fas fa-heart",
  "fas fa-hammer",
  "fas fa-award",
  "fas fa-cog",
  "fas fa-adjust",
  "far fa-bookmark",
  "far fa-calendar",
  "fas fa-clinic-medical",
  "fas fa-coffee",
  "fas fa-car-battery",
  "far fa-compass",
  "far fa-envelope",
  "fas fa-flask",
  "far fa-image",
  "fas fa-paint-brush",
  "far fa-paper-plane",
  "fas fa-plane",
]

const categories = [
  {
    id: "1",
    name: "EVE Information Portal",
    slug: "category",
    color: colors[0],
    icon: icons[0],
    children: [
      {
        id: "2",
        name: "Dev Blogs",
        slug: "category",
        color: colors[6],
        icon: icons[6],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "3",
        name: "Announcements",
        slug: "category",
        color: colors[7],
        icon: icons[7],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "4",
        name: "Community Fittings",
        slug: "category",
        color: colors[8],
        icon: icons[8],
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
    color: colors[2],
    icon: icons[2],
    children: [],
    depth: 0,
    parent: null,
  },
  {
    id: "6",
    name: "Communications Center",
    slug: "category",
    color: colors[3],
    icon: icons[3],
    children: [
      {
        id: "7",
        name: "General discussion",
        slug: "category",
        color: colors[9],
        icon: icons[9],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "8",
        name: "Crime & Punishment",
        slug: "category",
        color: colors[10],
        icon: icons[10],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "9",
        name: "Out Of Pod Experience",
        slug: "category",
        color: colors[11],
        icon: icons[11],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "10",
        name: "My EVE",
        slug: "category",
        color: colors[12],
        icon: icons[12],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "11",
        name: "Skill Discussion",
        slug: "category",
        color: colors[13],
        icon: icons[13],
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
    color: colors[4],
    icon: icons[4],
    children: [],
    depth: 0,
    parent: null,
  },
  {
    id: "13",
    name: "Events",
    slug: "category",
    color: colors[5],
    icon: icons[5],
    children: [
      {
        id: "14",
        name: "In Game Events",
        slug: "category",
        color: colors[14],
        icon: icons[14],
        children: [],
        depth: 1,
        parent: null,
      },
      {
        id: "15",
        name: "Out of Game Events",
        slug: "category",
        color: colors[15],
        icon: icons[15],
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