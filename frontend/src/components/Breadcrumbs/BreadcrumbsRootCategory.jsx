import classnames from "classnames"
import React from "react"
import { Link } from "react-router"

const BreadcrumbsRootCategory = ({ category, className }) => (
  <li className={classnames("breadcrumbs-item", className)}>
    <Link to={category.url.index}>
      <span className="material-icon">chevron_right</span>
      <span className="breadcrumbs-item-name">
        {category.special_role === "root_category"
          ? gettext("Threads")
          : gettext("Private threads")}
      </span>
    </Link>
  </li>
)

export default BreadcrumbsRootCategory
