import React from "react"
import Icon from "../Icon"
import { PaginatorProps } from "./Paginator.types"
import PaginatorButton from "./PaginatorButton"
import PaginatorDropdown from "./PaginatorDropdown"
import getPaginatorPagesList from "./getPaginatorPagesList"

const Paginator: React.FC<PaginatorProps> = ({ page, pages, url }) => (
  <div className="paginator paginator-full">
    <PaginatorButton
      className="btn-paginator-prev"
      page={page > 1 && page - 1}
      url={url}
    >
      <Icon icon="fas fa-angle-left" fixedWidth />
    </PaginatorButton>
    {getPaginatorPagesList(page, pages).map((i, key) =>
      i ? (
        <PaginatorButton
          className="btn-paginator-page"
          isActive={page === i}
          key={key}
          page={i}
          url={url}
        >
          {i}
        </PaginatorButton>
      ) : (
        <PaginatorButton className="btn-paginator-ellipsis" key={key}>
          ...
        </PaginatorButton>
      )
    )}
    <PaginatorButton
      className="btn-paginator-next"
      page={page < pages && page + 1}
      url={url}
    >
      <Icon icon="fas fa-angle-right" fixedWidth />
    </PaginatorButton>
    <PaginatorDropdown page={page} pages={pages} url={url} />
  </div>
)

export default React.memo(Paginator)
