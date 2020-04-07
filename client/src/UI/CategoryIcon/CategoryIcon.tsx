import React from "react"
import Icon from "../Icon"

interface ICategoryIconProps {
  className?: string
  category?: {
    color: string | null
    icon: string | null
  } | null
}

const CategoryIcon: React.FC<ICategoryIconProps> = ({ className, category }) => (
  <span
    className={className || "category-icon"}
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