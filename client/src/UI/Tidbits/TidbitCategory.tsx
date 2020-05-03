import classNames from "classnames"
import { Link } from "react-router-dom"
import React from "react"
import * as urls from "../../urls"
import TidbitItem from "./TidbitItem"

interface ITidbitCategoryProps {
  category: {
    id: string
    slug: string
    name: string
    color: string | null
  }
  parent?: boolean
}

const TidbitCategory: React.FC<ITidbitCategoryProps> = ({
  category,
  parent,
}) => (
  <TidbitItem
    className={classNames("tidbit-category", {
      "tidbit-parent-category": parent,
    })}
  >
    <Link to={urls.category(category)}>
      {category.color && (
        <span
          className="tidbit-category-color"
          style={{ backgroundColor: category.color }}
        />
      )}
      <span className="tidbit-category-name">{category.name}</span>
    </Link>
  </TidbitItem>
)

export default TidbitCategory
