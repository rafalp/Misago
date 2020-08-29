import React from "react"
import Icon from "../Icon"
import { IPaginatorProps } from "./Paginator.types"
import PaginatorButton from "./PaginatorButton"
import PaginatorDropdown from "./PaginatorDropdown"

const PaginatorCompact: React.FC<IPaginatorProps> = ({ page, pages, url }) => (
  <div className="paginator paginator-compact">
    <PaginatorButton
      className="btn-paginator-start"
      page={page > 1 && 1}
      url={url}
    >
      <Icon icon="fas fa-angle-double-left" fixedWidth />
    </PaginatorButton>
    <PaginatorButton
      className="btn-paginator-prev"
      page={page > 1 && page - 1}
      url={url}
    >
      <Icon icon="fas fa-angle-left" fixedWidth />
    </PaginatorButton>
    <PaginatorDropdown page={page} pages={pages} url={url} compact />
    <PaginatorButton
      className="btn-paginator-next"
      page={page < pages && page + 1}
      url={url}
    >
      <Icon icon="fas fa-angle-right" fixedWidth />
    </PaginatorButton>
    <PaginatorButton
      className="btn-paginator-last"
      page={page < pages && pages}
      url={url}
    >
      <Icon icon="fas fa-angle-double-right" fixedWidth />
    </PaginatorButton>
  </div>
)

export default React.memo(PaginatorCompact)
