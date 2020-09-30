import React from "react"
import { RootContainer, categories } from "../../../UI/Storybook"
import ThreadsHeaderAll from "./ThreadsHeaderAll"
import ThreadsHeaderCategory from "./ThreadsHeaderCategory"

export default {
  title: "Route/Threads/Header",
}

const forumStats = { threads: 142567, posts: 1089524, users: 25663 }

export const Category = () => (
  <RootContainer>
    <ThreadsHeaderCategory category={categories[0]} />
  </RootContainer>
)

export const ForumIndex = () => (
  <RootContainer>
    <ThreadsHeaderAll
      settings={{
        forumIndexThreads: true,
        forumIndexHeader: "Welcome to Misago official forums!",
        forumName: "Misago",
      }}
      stats={forumStats}
    />
  </RootContainer>
)

export const AllThreads = () => (
  <RootContainer>
    <ThreadsHeaderAll
      settings={{
        forumIndexThreads: false,
        forumIndexHeader: "",
        forumName: "Misago",
      }}
      stats={forumStats}
    />
  </RootContainer>
)
