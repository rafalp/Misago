import classnames from "classnames"
import React from "react"

const BreadcrumbsCategory = ({ category, className }) => (
  <li className={classnames("breadcrumbs-item", className)}>
    <a href={category.url.index}>
      <span
        className="material-icon"
        style={{ color: category.color || "inherit" }}
      >
        label
      </span>
      <span className="breadcrumbs-item-name">{category.name}</span>
    </a>
  </li>
)

export default BreadcrumbsCategory
