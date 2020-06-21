import React from "react"
import { Link } from "react-router-dom"
import { ButtonSecondary } from "../Button"
import Icon from "../Icon"

interface IPaginatorButtonProps {
  icon: string
  page?: number | null | false
  url: (page: number) => string
}

const PaginatorButton: React.FC<IPaginatorButtonProps> = ({
  icon,
  page,
  url,
}) =>
  page ? (
    <Link className="btn btn-secondary btn-responsive" to={url(page)}>
      <Icon icon={icon} fixedWidth solid />
    </Link>
  ) : (
    <ButtonSecondary icon={icon} iconSolid disabled responsive />
  )

export default PaginatorButton
