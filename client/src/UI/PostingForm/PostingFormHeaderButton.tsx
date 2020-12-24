import classnames from "classnames"
import React from "react"
import Icon from "../Icon"

interface PostingFormHeaderButtonProps {
  className?: string
  icon: string
  onClick?: () => void
}

const PostingFormHeaderButton: React.FC<PostingFormHeaderButtonProps> = ({
  className,
  icon,
  onClick,
}) => (
  <button
    className={classnames("btn btn-posting-form-header btn-sm", className)}
    type="button"
    onClick={onClick}
  >
    <Icon icon={icon} fixedWidth />
  </button>
)

export default PostingFormHeaderButton
