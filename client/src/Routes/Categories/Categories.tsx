import React from "react"
import { Link } from "react-router-dom"

import { RouteGraphQLError, RouteLoader } from "../../UI"
import * as urls from "../../urls"
import useCategoriesQuery from "./useCategoriesQuery"

const Categories: React.FC = () => {
  const { data, error, loading } = useCategoriesQuery()

  if (loading) return <RouteLoader />
  if (error) return <RouteGraphQLError error={error} />

  return (
    <ul>
      {data?.categories.map(category => (
        <li key={category.id}>
          <Link to={urls.category(category)}>{category.name}</Link>
          {category.children.length && (
            <ul>
              {category.children.map(child => (
                <li key={child.id}>
                  <Link to={urls.category(child)}>{child.name}</Link>
                </li>
              ))}
            </ul>
          )}
        </li>
      ))}
    </ul>
  )
}

export default Categories
