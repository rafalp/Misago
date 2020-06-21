import React from "react"
import { Link } from "react-router-dom"

interface IPaginatorButtonProps {
  children: React.ReactNode
  page?: number | null | false
  url: (page: number) => string
}

const PaginatorButton: React.FC<IPaginatorButtonProps> = ({
  children,
  page,
  url,
}) =>
  page ? (
    <Link className="btn btn-secondary btn-responsive" to={url(page)}>
      {children}
    </Link>
  ) : (
    <button
      className="btn btn-secondary btn-responsive"
      type="button"
      disabled
    >
      {children}
    </button>
  )

export default PaginatorButton
