import { action } from "@storybook/addon-actions"
import React from "react"
import { Layout, LayoutMain, LayoutSide } from "../../../UI"
import { RootContainer, categories } from "../../../UI/Storybook"
import { IThread, IThreadCategory } from "../Threads.types"
import ThreadsList from "./ThreadsList"

export default {
  title: "Route/Threads/ThreadsList",
}

const fetch = action("fetch")

const threads = (items?: Array<IThread> | null) => {
  if (items) return { items, nextCursor: null }
  return { items: [], nextCursor: null }
}

const thread = (data?: {
  id: string
  title?: string
  category?: IThreadCategory
}): IThread => {
  return Object.assign(
    {
      id: "1",
      title: "Test thread",
      slug: "test-thread",
      category: { ...categories[0], parent: categories[1] },
    },
    data || {}
  )
}

const Container: React.FC<{ children: React.ReactNode }> = ({ children }) => (
  <RootContainer padding>
    <Layout>
      <LayoutSide />
      <LayoutMain>{children}</LayoutMain>
    </Layout>
  </RootContainer>
)

export const Threads = () => (
  <Container>
    <ThreadsList
      threads={threads([
        thread({
          id: "1",
          title: "The atmosphere has many layers with different temperatures.",
          category: categories[1],
        }),
        thread({
          id: "2",
          title:
            "Instead, in 2006, the International Astronomical Union created a new class of objects called dwarf planets, and placed Pluto, Eris and the asteroid Ceres in this category.",
        }),
      ])}
      loading={false}
      update={{
        fetch,
        threads: 0,
        loading: false,
      }}
    />
  </Container>
)

export const WithUpdate = () => (
  <Container>
    <h5>Update available</h5>
    <ThreadsList
      threads={threads([thread()])}
      loading={false}
      update={{
        fetch,
        threads: 7,
        loading: false,
      }}
    />
    <h5>Update loading</h5>
    <ThreadsList
      threads={threads([thread()])}
      loading={false}
      update={{
        fetch,
        threads: 7,
        loading: true,
      }}
    />
    <h5>Update disabled</h5>
    <ThreadsList
      threads={threads([thread()])}
      loading={true}
      update={{
        fetch,
        threads: 7,
        loading: false,
      }}
    />
  </Container>
)

export const Loading = () => (
  <Container>
    <ThreadsList
      threads={null}
      loading={true}
      update={{
        fetch,
        threads: 0,
        loading: false,
      }}
    />
  </Container>
)

export const LoadingMore = () => (
  <Container>
    <ThreadsList
      threads={threads([thread()])}
      loading={true}
      update={{
        fetch,
        threads: 0,
        loading: false,
      }}
    />
  </Container>
)

export const Empty = () => (
  <Container>
    <ThreadsList
      threads={threads()}
      loading={false}
      update={{
        fetch,
        threads: 0,
        loading: false,
      }}
    />
  </Container>
)
