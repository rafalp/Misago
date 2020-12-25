import React from "react"
import Responsive from "../../../UI/Responsive"
import ThreadBreadcrumbsItem from "./ThreadBreadcrumbsItem"

interface ThreadBreadcrumbsProps {
  category: {
    id: string
    name: string
    slug: string
    icon: string | null
    color: string | null
    parent: {
      id: string
      name: string
      slug: string
      icon: string | null
      color: string | null
    } | null
  }
}

const ThreadBreadcrumbs: React.FC<ThreadBreadcrumbsProps> = ({
  category,
}) => (
  <Responsive className="thread-breadcrumbs" mobile>
    <div className="row">
      {category.parent && (
        <div className="col-6">
          <ThreadBreadcrumbsItem category={category.parent} />
        </div>
      )}
      <div className={category.parent ? "col-6" : "col"}>
        <ThreadBreadcrumbsItem category={category} />
      </div>
    </div>
  </Responsive>
)

export default ThreadBreadcrumbs
