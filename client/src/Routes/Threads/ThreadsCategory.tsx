import classNames from "classnames"
import React from "react"
import { useParams } from "react-router-dom"
import { RouteNotFound, WindowTitle } from "../../UI"
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
  const { data, error, loading } = useCategoryThreadsQuery({ id })

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
      <ThreadsList error={error} loading={loading} threads={threads} />
    </ThreadsLayout>
  )
}

export default ThreadsCategory
