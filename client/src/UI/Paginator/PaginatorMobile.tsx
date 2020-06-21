import React from "react"
import Icon from "../Icon"
import { IPaginatorProps } from "./Paginator.types"
import PaginatorButton from "./PaginatorButton"

const PaginatorMobile: React.FC<IPaginatorProps> = ({ page, url }) => (
  <div className="paginator">
    <PaginatorButton page={page && page.number > 1 && 1} url={url}>
      <Icon icon="angle-double-left" solid fixedWidth />
    </PaginatorButton>
    <PaginatorButton
      page={page && page.number > 1 && page.number - 1}
      url={url}
    >
      <Icon icon="angle-left" solid fixedWidth />
    </PaginatorButton>
    <PaginatorButton
      page={page && page.number < page.pagination.pages && page.number + 1}
      url={url}
    >
      <Icon icon="angle-right" solid fixedWidth />
    </PaginatorButton>
    <PaginatorButton
      page={
        page && page.number < page.pagination.pages && page.pagination.pages
      }
      url={url}
    >
      <Icon icon="angle-double-right" solid fixedWidth />
    </PaginatorButton>
  </div>
)

export default React.memo(PaginatorMobile)
