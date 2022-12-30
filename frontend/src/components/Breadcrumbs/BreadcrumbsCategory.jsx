import classnames from "classnames"
import React from "react"
import { Link } from "react-router"

const BreadcrumbsCategory = ({ category, list, className }) => (
  <li className={classnames("breadcrumbs-item", className)}>
    <Link to={category.url.index + (list ? list.path : "")}>
      <span
        className="material-icon"
        style={{ color: category.color || "inherit" }}
      >
        label
      </span>
      <span className="breadcrumbs-item-name">{category.name}</span>
    </Link>
  </li>
)

export default BreadcrumbsCategory
