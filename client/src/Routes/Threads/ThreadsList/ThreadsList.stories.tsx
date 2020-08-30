import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import { ApolloError } from "apollo-client"
import React from "react"
import { Layout, LayoutMain, LayoutSide } from "../../../UI"
import { RootContainer, categories } from "../../../UI/Storybook"
import { IThread, IThreadPoster, IThreadCategory } from "../Threads.types"
import ThreadsList from "./ThreadsList"
import useThreadsSelection from "../useThreadsSelection"

export default {
  title: "Route/Threads/ThreadsList",
  decorators: [withKnobs],
}

const fetch = action("fetch")

const threads = (items?: Array<IThread> | null) => {
  if (items) return { items, nextCursor: null }
  return { items: [], nextCursor: null }
}

const thread = (data?: {
  id: string
  title?: string
  slug?: string
  category?: IThreadCategory
  starter?: IThreadPoster | null
  starterName?: string
  lastPoster?: IThreadPoster | null
  lastPosterName?: string
  startedAt?: string
  lastPostedAt?: string
  replies?: number
  isClosed?: boolean
}): IThread => {
  return Object.assign(
    {
      id: "1",
      title: "Test thread",
      slug: "test-thread",
      startedAt: "2020-05-01T10:49:02.159Z",
      lastPostedAt: "2020-05-02T12:38:41.159Z",
      starterName: "LoremIpsum",
      starter: null,
      lastPosterName: "DolorMet",
      lastPoster: null,
      category: { ...categories[0], parent: categories[1] },
      replies: 0,
      isClosed: false,
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

export const Threads = () => {
  const now = new Date()
  const items = threads([
    thread({
      id: "1",
      title: "The atmosphere has many layers with different temperatures.",
      category: categories[1],
      replies: 58102,
      isClosed: true,
    }),
    thread({
      id: "2",
      title:
        "Instead, in 2006, the International Astronomical Union created a new class of objects called dwarf planets, and placed Pluto, Eris and the asteroid Ceres in this category.",
      lastPosterName: "LoremIpsumDolorMet",
      lastPostedAt: new Date(now.getTime() - 36 * 3600 * 1000).toUTCString(),
    }),
    thread({
      id: "3",
      title:
        "ReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReReRe",
    }),
  ])

  const selection = useThreadsSelection(items.items)

  return (
    <Container>
      <ThreadsList
        threads={items}
        selectable={boolean("Moderation", false)}
        selection={selection}
        loading={false}
      />
    </Container>
  )
}

export const WithUpdate = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <h5>Update available</h5>
      <ThreadsList
        selection={selection}
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
        selection={selection}
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
        selection={selection}
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
}

export const Loading = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <ThreadsList threads={null} selection={selection} loading={true} />
    </Container>
  )
}

export const LoadingMore = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <ThreadsList
        threads={threads([thread()])}
        selection={selection}
        loading={true}
      />
    </Container>
  )
}

export const Empty = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <ThreadsList threads={threads()} selection={selection} loading={false} />
    </Container>
  )
}

export const QueryError = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <ThreadsList
        error={new ApolloError({})}
        threads={null}
        selection={selection}
        loading={false}
      />
    </Container>
  )
}

export const NetworkError = () => {
  const selection = useThreadsSelection()

  return (
    <Container>
      <ThreadsList
        error={new ApolloError({ networkError: new Error() })}
        threads={null}
        selection={selection}
        loading={false}
      />
    </Container>
  )
}
