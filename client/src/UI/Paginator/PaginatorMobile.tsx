import React from "react"
import Icon from "../Icon"
import { IPaginatorProps } from "./Paginator.types"
import PaginatorButton from "./PaginatorButton"
import PaginatorDropdown from "./PaginatorDropdown"

const PaginatorMobile: React.FC<IPaginatorProps> = ({ page, pages, url }) => (
  <div className="paginator paginator-md">
    <PaginatorButton page={page > 1 && 1} url={url}>
      <Icon icon="angle-double-left" solid fixedWidth />
    </PaginatorButton>
    <PaginatorButton page={page > 1 && page - 1} url={url}>
      <Icon icon="angle-left" solid fixedWidth />
    </PaginatorButton>
    <PaginatorDropdown page={page} pages={pages} url={url} />
    <PaginatorButton page={page < pages && page + 1} url={url}>
      <Icon icon="angle-right" solid fixedWidth />
    </PaginatorButton>
    <PaginatorButton page={page < pages && pages} url={url}>
      <Icon icon="angle-double-right" solid fixedWidth />
    </PaginatorButton>
  </div>
)

export default React.memo(PaginatorMobile)
