import React from "react"

const ThreadsListItemCategory = ({ parent, category }) => (
  <span>
    {parent && (
      <a
        href={parent.url.index}
        className={getClassName(parent) + " threads-list-item-parent-category"}
        style={parent.color ? { "--label-color": parent.color } : null}
        title={!!parent.short_name ? parent.name : null}
      >
        {parent.short_name || parent.name}
      </a>
    )}
    <a
      href={category.url.index}
      className={getClassName(category)}
      style={category.color ? { "--label-color": category.color } : null}
      title={!!category.short_name ? category.name : null}
    >
      {category.short_name || category.name}
    </a>
  </span>
)

const getClassName = (category) => {
  let className = "threads-list-item-category threads-list-category-label"

  if (category.color) {
    className += " threads-list-category-label-color"
  }

  return className
}

export default ThreadsListItemCategory
