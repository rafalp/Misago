import React from "react"
import { Link } from "react-router-dom"
import CategoryIcon from "../../../UI/CategoryIcon"
import * as urls from "../../../urls"

interface IThreadBreadcrumbsItemProps {
  category: {
    id: string
    name: string
    slug: string
    icon: string | null
    color: string | null
  }
}

const ThreadBreadcrumbsItem: React.FC<IThreadBreadcrumbsItemProps> = ({
  category,
}) => (
  <Link
    className="btn btn-secondary btn-sm thread-breadcrumb"
    to={urls.category(category)}
  >
    <CategoryIcon category={category} className="thread-breadcrumb-icon" />
    <span className="thread-breadcrumb-name">{category.name}</span>
  </Link>
)

export default ThreadBreadcrumbsItem
