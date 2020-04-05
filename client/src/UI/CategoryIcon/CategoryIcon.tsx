import React from "react"
import Icon from "../Icon"

interface ICategoryIconProps {
  category?: {
    color: string | null
    icon: string | null
  } | null
}

const CategoryIcon: React.FC<ICategoryIconProps> = ({ category }) => (
  <span
    className="nav-link-category-icon"
    style={category?.color ? { color: category.color } : undefined}
  >
    {category?.icon ? (
      <i className={category.icon + " fa-fw"} />
    ) : (
      <Icon icon="comment-alt" fixedWidth />
    )}
  </span>
)

export default CategoryIcon