import classNames from "classnames"
import React from "react"
import { useParams } from "react-router-dom"
import { RouteNotFound, ViewportEvent, WindowTitle } from "../../UI"
import { HeaderCategory } from "./Header"
import LoadMoreButton from "./LoadMoreButton"
import { IThreadsProps } from "./Threads.types"
import ThreadsLayout from "./ThreadsLayout"
import ThreadsList from "./ThreadsList"
import useActiveCategory from "./useActiveCategory"
import { useCategoryThreadsQuery } from "./useThreadsQuery"

interface IThreadsCategoryParams {
  id: string
  slug: string
}

const ThreadsCategory: React.FC<IThreadsProps> = ({ openCategoryPicker }) => {
  const { id } = useParams<IThreadsCategoryParams>()
  const activeCategory = useActiveCategory(id)
  const { data, error, loading, fetchMoreThreads } = useCategoryThreadsQuery({
    id,
  })

  const { category } = activeCategory || { category: null }
  const { threads } =
    data && data.category.id === id ? data : { threads: null }

  if (data && !data.category) return <RouteNotFound />

  return (
    <ThreadsLayout
      className={
        category
          ? classNames(
              "route-category",
              category && `route-category-${category.id}`
            )
          : undefined
      }
      category={activeCategory}
      openCategoryPicker={openCategoryPicker}
    >
      {category && (
        <>
          <WindowTitle title={category.name} />
          <HeaderCategory category={category} />
        </>
      )}
      <ViewportEvent disabled={loading} onEnter={fetchMoreThreads} desktopOnly>
        <ThreadsList error={error} loading={loading} threads={threads} />
      </ViewportEvent>
      {threads && threads.nextCursor && (
        <LoadMoreButton loading={loading} onClick={fetchMoreThreads} />
      )}
    </ThreadsLayout>
  )
}

export default ThreadsCategory
