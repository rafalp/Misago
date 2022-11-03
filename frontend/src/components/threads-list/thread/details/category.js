import React from "react"

export default function({ category, className }) {
  if (!category) return null

  className += " category-label"
  if (category.color) {
    className += " category-label-color"
  } else {
    className += " category-label-no-color"
  }

  if (category.css_class) {
    className += " thread-detail-category-" + category.css_class
  }

  return (
    <a
      className={className}
      style={{ backgroundColor: category.color }}
      title={category.short_name ? category.name : null}
      href={category.url.index}
    >
      {category.short_name || category.name}
    </a>
  )
}
