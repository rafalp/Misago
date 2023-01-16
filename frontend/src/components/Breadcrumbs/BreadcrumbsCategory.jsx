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
      {!!category.short_name && (
        <span
          className="breadcrumbs-item-name hidden-sm hidden-md hidden-lg"
          title={category.name}
        >
          {category.short_name}
        </span>
      )}
      {!!category.short_name && (
        <span className="breadcrumbs-item-name hidden-xs">{category.name}</span>
      )}
      {!category.short_name && (
        <span className="breadcrumbs-item-name">{category.name}</span>
      )}
    </a>
  </li>
)

export default BreadcrumbsCategory
