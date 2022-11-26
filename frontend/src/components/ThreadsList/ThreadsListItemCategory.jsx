import React from "react"

const ThreadsListItemCategory = ({ category }) => (
  <a
    href={category.url.index}
    className={getClassName(category)}
    style={category.color ? {"--label-color": category.color} : null}
    title={!!category.short_name ? category.name : null}
  >
    {category.short_name || category.name}
  </a>
)

const getClassName = (category) => {
  let className = "threads-list-item-category"
  className += " threads-list-category-label"

  if (category.color) {
    className += " threads-list-category-label-color"
  }

  return className
}

export default ThreadsListItemCategory