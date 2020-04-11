import classNames from "classnames"
import React from "react"
import { Link, useParams } from "react-router-dom"
import {
  CategoriesNav,
  Layout,
  LayoutMain,
  LayoutSide,
  RouteContainer,
  RouteGraphQLError,
  RouteLoader,
  RouteNotFound,
  WindowTitle,
} from "../../UI"
import * as urls from "../../urls"
import { CategoryHeader } from "./Header"
import { MobileCategoryNavButton } from "./MobileCategoryNav"
import { IThreadsListProps } from "./Threads.types"
import useActiveCategory from "./useActiveCategory"
import { useCategoryThreadsQuery } from "./useThreadsQuery"

interface ICategoryThreadsListParams {
  id: string
  slug: string
}

const CategoryThreadsList: React.FC<IThreadsListProps> = ({
  openCategoryPicker,
}) => {
  const { id } = useParams<ICategoryThreadsListParams>()
  const activeCategory = useActiveCategory(id)
  const { data, error, loading } = useCategoryThreadsQuery({ id })

  if (loading) return <RouteLoader />
  if (!data && error) return <RouteGraphQLError error={error} />
  if (!data || !data?.category) return <RouteNotFound />

  const { category } = activeCategory || { category: null }
  const { threads } = data || { threads: null }

  return (
    <RouteContainer
      className={classNames(
        "route-category",
        category && `route-category-${category.id}`
      )}
    >
      <Layout>
        <LayoutSide>
          <CategoriesNav active={activeCategory} />
        </LayoutSide>
        <LayoutMain>
          {category ? (
            <>
              <WindowTitle title={category.name} />
              <MobileCategoryNavButton
                active={category}
                onClick={() => openCategoryPicker(activeCategory)}
              />
              <CategoryHeader category={category} />
              <ul>
                {threads.items.map((thread) => (
                  <li key={thread.id}>
                    <strong>
                      <Link to={urls.thread(thread)}>{thread.title}</Link>
                    </strong>
                    <ul className="list-inline">
                      {thread.category.parent && (
                        <li className="list-inline-item">
                          <Link
                            to={urls.category(thread.category.parent)}
                            style={{
                              borderLeft: `4px solid ${thread.category.parent.color}`,
                            }}
                          >
                            {thread.category.parent.name}
                          </Link>
                        </li>
                      )}
                      <li className="list-inline-item">
                        <Link
                          to={urls.category(thread.category)}
                          style={{
                            borderLeft: `4px solid ${thread.category.color}`,
                          }}
                        >
                          {thread.category.name}
                        </Link>
                      </li>
                    </ul>
                  </li>
                ))}
              </ul>
            </>
          ) : (
            <>CATEGORY NOT FOUND</>
          )}
        </LayoutMain>
      </Layout>
    </RouteContainer>
  )
}

export default CategoryThreadsList
