import { actions } from "@storybook/addon-actions"
import React from "react"
import { CategoriesContext } from "../../Context"
import { LoadMoreButton } from "../../UI"
import { categories, settingsFactory } from "../../UI/Storybook"
import { ThreadsHeaderAll, ThreadsHeaderCategory } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import ThreadsToolbar from "./ThreadsToolbar"

export default {
  title: "Route/Threads/FullPage",
}

const { openCategoryPicker, loadMore } = actions({
  openCategoryPicker: "open category picker",
  loadMore: "load more threads",
})

export const AllThreads = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsLayout openCategoryPicker={openCategoryPicker}>
      <ThreadsHeaderAll
        settings={settingsFactory()}
        stats={{ threads: 142567, posts: 1089524, users: 25663 }}
      />
      <ThreadsToolbar />
      <ThreadsList loading={true} threads={null} />
      <LoadMoreButton
        data={{ nextCursor: "true" }}
        loading={false}
        onEvent={loadMore}
      />
    </ThreadsLayout>
  </CategoriesContext.Provider>
)

export const Category = () => (
  <CategoriesContext.Provider value={categories}>
    <ThreadsLayout openCategoryPicker={openCategoryPicker}>
      <ThreadsHeaderCategory category={categories[1]} />
      <ThreadsToolbar />
      <ThreadsList loading={true} threads={null} />
      <LoadMoreButton
        data={{ nextCursor: "true" }}
        loading={false}
        onEvent={loadMore}
      />
    </ThreadsLayout>
  </CategoriesContext.Provider>
)
