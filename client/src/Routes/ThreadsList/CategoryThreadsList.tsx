import React from "react"
import { Link, useParams } from "react-router-dom"
import { RouteGraphQLError, RouteLoader, RouteNotFound } from "../../UI"
import * as urls from "../../urls"
import { useCategoryThreadsQuery } from "./useThreadsQuery"

interface ICategoryThreadsListParams {
  id: string
  slug: string
}

const CategoryThreadsList: React.FC = () => {
  const { id } = useParams<ICategoryThreadsListParams>()
  const { data, error, loading } = useCategoryThreadsQuery({ id })

  if (loading) return <RouteLoader />
  if (error) return <RouteGraphQLError error={error} />
  if (!data?.category) return <RouteNotFound />

  return (
    <div>
      <Link to={urls.categories()}>[CATEGORIES]</Link>
      <Link to={urls.startThread()}>[START THREAD]</Link>
      <h1>{data?.category.name}</h1>
      <ul>
        {data?.threads.items.map(thread => (
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
                  style={{ borderLeft: `4px solid ${thread.category.color}` }}
                >
                  {thread.category.name}
                </Link>
              </li>
            </ul>
          </li>
        ))}
      </ul>
    </div>
  )
}

export default CategoryThreadsList
