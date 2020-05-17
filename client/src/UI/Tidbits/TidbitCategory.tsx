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
  disabled?: boolean
  parent?: boolean
}

const TidbitCategory: React.FC<ITidbitCategoryProps> = ({
  category,
  disabled,
  parent,
}) => (
  <TidbitItem
    className={classNames("tidbit-category", {
      "tidbit-parent-category": parent,
    })}
  >
    {disabled ? (
      <TidbitCategoryContent category={category} />
    ) : (
      <Link to={urls.category(category)}>
        <TidbitCategoryContent category={category} />
      </Link>
    )}
  </TidbitItem>
)

interface ITidbitCategoryContentProps {
  category: {
    id: string
    slug: string
    name: string
    color: string | null
  }
}

const TidbitCategoryContent: React.FC<ITidbitCategoryContentProps> = ({
  category,
}) => (
  <>
    {category.color && (
      <span
        className="tidbit-category-color"
        style={{ backgroundColor: category.color }}
      />
    )}
    <span className="tidbit-category-name">{category.name}</span>
  </>
)

export default TidbitCategory
