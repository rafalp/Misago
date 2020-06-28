import classnames from "classnames"
import React from "react"
import { Link } from "react-router-dom"

interface IPaginatorButtonProps {
  className?: string
  children: React.ReactNode
  page?: number | null | false
  title?: string
  isActive?: boolean
  url?: (page: number) => string
}

const PaginatorButton: React.FC<IPaginatorButtonProps> = ({
  className,
  children,
  page,
  title,
  isActive,
  url,
}) =>
  page && url ? (
    <Link
      className={classnames(
        "btn",
        "btn-secondary",
        "btn-responsive",
        { "btn-paginator-page-active": isActive },
        className
      )}
      title={title}
      to={url(page)}
    >
      {children}
    </Link>
  ) : (
    <button
      className={classnames(
        "btn",
        { "btn-primary": isActive, "btn-secondary": !isActive },
        "btn-responsive",
        className
      )}
      type="button"
      disabled
    >
      {children}
    </button>
  )

export default PaginatorButton
