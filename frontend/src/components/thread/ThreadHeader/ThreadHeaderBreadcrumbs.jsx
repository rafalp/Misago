import React from "react"
import {
  Breadcrumbs,
  BreadcrumbsCategory,
  BreadcrumbsRootCategory,
} from "../../Breadcrumbs"

const ThreadHeaderBreadcrumbs = ({ breadcrumbs }) => (
  <Breadcrumbs>
    {breadcrumbs.map((category) =>
      category.special_role ? (
        <BreadcrumbsRootCategory key={category.id} category={category} />
      ) : (
        <BreadcrumbsCategory key={category.id} category={category} />
      )
    )}
  </Breadcrumbs>
)

export default ThreadHeaderBreadcrumbs
