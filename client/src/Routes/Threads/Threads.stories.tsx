import { action } from "@storybook/addon-actions"
import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import { CategoriesContext } from "../../Context"
import LoadMoreButton from "../../UI/LoadMoreButton"
import {
  SettingsContextFactory,
  categories,
  settingsFactory,
} from "../../UI/Storybook"
import { ThreadsHeaderAll, ThreadsHeaderCategory } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import ThreadsToolbar from "./ThreadsToolbar"
import useThreadsSelection from "./useThreadsSelection"

export default {
  title: "Route/Threads/FullPage",
  decorators: [withKnobs],
}

const loadMore = action("load more threads")

export const AllThreads = () => {
  const acl = { start: true }

  return (
    <SettingsContextFactory>
      <CategoriesContext.Provider value={categories}>
        <ThreadsLayout>
          <ThreadsHeaderAll
            settings={settingsFactory()}
            stats={{ threads: 142567, posts: 1089524, users: 25663 }}
          />
          <ThreadsToolbar acl={acl} />
          <ThreadsList
            acl={acl}
            loading={true}
            threads={null}
            selection={useThreadsSelection()}
          />
          <LoadMoreButton
            data={{ nextCursor: "true" }}
            loading={false}
            onEvent={loadMore}
          />
        </ThreadsLayout>
      </CategoriesContext.Provider>
    </SettingsContextFactory>
  )
}

export const Category = () => {
  const acl = { start: boolean("acl.start", true) }
  return (
    <SettingsContextFactory>
      <CategoriesContext.Provider value={categories}>
        <ThreadsLayout
          activeCategory={{ category: categories[1], parent: categories[1] }}
        >
          <ThreadsHeaderCategory category={categories[1]} />
          <ThreadsToolbar acl={acl} category={categories[1]} />
          <ThreadsList
            acl={acl}
            loading={true}
            threads={null}
            selection={useThreadsSelection()}
          />
          <LoadMoreButton
            data={{ nextCursor: "true" }}
            loading={false}
            onEvent={loadMore}
          />
        </ThreadsLayout>
      </CategoriesContext.Provider>
    </SettingsContextFactory>
  )
}
