import React from "react"
import CategoryButton from "../../../UI/CategoryButton"
import * as urls from "../../../urls"

interface ThreadBreadcrumbsItemProps {
  category: {
    id: string
    name: string
    slug: string
    icon: string | null
    color: string | null
  }
}

const ThreadBreadcrumbsItem: React.FC<ThreadBreadcrumbsItemProps> = ({
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
