import React from "react"
import PaginatorButton from "./PaginatorButton"

interface IPaginatorProps {
  page?: {
    number: number
    pagination: {
      pages: number
    }
  } | null
  url: (page: number) => string
}

const Paginator: React.FC<IPaginatorProps> = ({ page, url }) => (
  <div className="paginator">
    <PaginatorButton
      icon="angle-double-left"
      page={page && page.number > 1 && 1}
      url={url}
    />
    <PaginatorButton
      icon="angle-left"
      page={page && page.number > 1 && page.number - 1}
      url={url}
    />
    <PaginatorButton
      icon="angle-right"
      page={page && page.number < page.pagination.pages && page.number + 1}
      url={url}
    />
    <PaginatorButton
      icon="angle-double-right"
      page={
        page && page.number < page.pagination.pages && page.pagination.pages
      }
      url={url}
    />
  </div>
)

export default Paginator
