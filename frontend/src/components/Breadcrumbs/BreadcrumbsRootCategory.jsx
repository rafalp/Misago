import classnames from "classnames"
import React from "react"

const BreadcrumbsRootCategory = ({ category, className }) => (
  <li className={classnames("breadcrumbs-item", className)}>
    <a href={category.url.index}>
      <span className="material-icon">chevron_right</span>
      <span className="breadcrumbs-item-name">
        {category.special_role === "root_category"
          ? pgettext("breadcrumb", "Threads")
          : pgettext("breadcrumb", "Private threads")}
      </span>
    </a>
  </li>
)

export default BreadcrumbsRootCategory
