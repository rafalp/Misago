import classNames from "classnames"
import React from "react"
import { useParams } from "react-router-dom"
import { LoadMoreButton, RouteNotFound, WindowTitle } from "../../UI"
import { ThreadsHeaderCategory } from "./ThreadsHeader"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import { useThreadsModeration } from "./ThreadsModeration"
import ThreadsToolbar from "./ThreadsToolbar"
import useActiveCategory from "./useActiveCategory"
import { useCategoryThreadsQuery } from "./useThreadsQuery"
import useThreadsSelection from "./useThreadsSelection"

interface IThreadsCategoryParams {
  id: string
  slug: string
}

const ThreadsCategory: React.FC = () => {
  const { id } = useParams<IThreadsCategoryParams>()
  const activeCategory = useActiveCategory(id)
  const {
    data,
    error,
    loading,
    update,
    fetchMoreThreads,
  } = useCategoryThreadsQuery({
    id,
  })

  const { category } = activeCategory || { category: null }
  const { threads } =
    data && data.category.id === id ? data : { threads: null }

  const selection = useThreadsSelection(threads?.items || [])
  const moderation = useThreadsModeration(selection.selected)

  if (data && !data.category) return <RouteNotFound />

  return (
    <ThreadsLayout
      activeCategory={activeCategory}
      className={
        category
          ? classNames(
              "route-category",
              category && `route-category-${category.id}`
            )
          : undefined
      }
    >
      {category && (
        <>
          <WindowTitle title={category.name} alerts={update.threads} />
          <ThreadsHeaderCategory category={category} />
          <ThreadsToolbar
            category={category}
            moderation={moderation}
            selection={selection}
          />
        </>
      )}
      <ThreadsList
        category={category}
        error={error}
        loading={loading}
        selectable={!!moderation}
        selection={selection}
        threads={threads}
        update={update}
      />
      <LoadMoreButton
        data={threads}
        loading={loading}
        onEvent={fetchMoreThreads}
      />
    </ThreadsLayout>
  )
}

export default ThreadsCategory
