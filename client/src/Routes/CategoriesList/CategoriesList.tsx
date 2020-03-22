import React from "react"
import { Link } from "react-router-dom"

import { RouteGraphQLError, RouteLoader } from "../../UI"
import * as urls from "../../urls"
import useCategoriesQuery from "./useCategoriesQuery"

const CategoriesList: React.FC = () => {
  const { data, error, loading } = useCategoriesQuery()

  if (loading) return <RouteLoader />
  if (error) return <RouteGraphQLError error={error} />

  return (
    <ul>
      {data?.categories.map(category => (
        <li key={category.id}>
          <Link
            to={urls.category(category)}
            style={{ borderLeft: `4px solid ${category.color}` }}
          >
            {category.name}
          </Link>
          {category.children.length && (
            <ul>
              {category.children.map(child => (
                <li key={child.id}>
                  <Link
                    to={urls.category(child)}
                    style={{ borderLeft: `4px solid ${child.color}` }}
                  >
                    {child.name}
                  </Link>
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  )
}

export default CategoriesList
