import classNames from "classnames"
import React from "react"
import { useParams } from "react-router-dom"
import { LoadMoreButton, RouteNotFound, WindowTitle } from "../../UI"
import { HeaderCategory } from "./Header"
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
          <WindowTitle title={category.name} alerts={update.threads} />
          <HeaderCategory category={category} />
        </>
      )}
      <ThreadsList
        error={error}
        loading={loading}
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
