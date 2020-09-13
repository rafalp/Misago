import React from "react"
import CategoryButton from "../../../UI/CategoryButton"
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
  <CategoryButton
    category={category}
    link={urls.category(category)}
    nowrap
    small
  />
)

export default ThreadBreadcrumbsItem
