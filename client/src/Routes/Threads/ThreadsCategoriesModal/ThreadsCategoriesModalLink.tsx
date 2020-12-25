import classnames from "classnames"
import React from "react"
import { Link } from "react-router-dom"
import { ButtonLink } from "../../../UI/Button"
import CategoryIcon from "../../../UI/CategoryIcon"

interface ThreadsCategoriesModalLinkProps {
  category?: {
    color: string | null
    icon: string | null
  } | null
  to: string
  text: React.ReactNode
  isActive?: boolean
  isChild?: boolean
  isOpen?: boolean
  hasChildren?: boolean
  toggle?: () => void
}

const ThreadsCategoriesModalLink: React.FC<ThreadsCategoriesModalLinkProps> = ({
  category,
  to,
  text,
  isActive,
  isChild,
  isOpen,
  hasChildren,
  toggle,
}) => (
  <>
    <Link
      className={classnames(
        "btn btn-link",
        isChild ? "btn-subcategory" : "btn-category",
        { active: isActive }
      )}
      to={to}
    >
      <CategoryIcon className="btn-category-icon" category={category} />
      <span className="btn-text">{text}</span>
    </Link>
    {hasChildren && (
      <ButtonLink
        icon={isOpen ? "far fa-minus-square" : "far fa-plus-square"}
        onClick={toggle}
      />
    )}
  </>
)

export default ThreadsCategoriesModalLink
