import React from "react"
import Icon from "../Icon"

interface IPostingFormHeaderButtonProps {
  icon: string
  onClick?: () => void
}

const PostingFormHeaderButton: React.FC<IPostingFormHeaderButtonProps> = ({
  icon,
  onClick,
}) => (
  <button
    className="btn btn-posting-form-header btn-sm"
    type="button"
    onClick={onClick}
  >
    <Icon icon={icon} fixedWidth />
  </button>
)

export default PostingFormHeaderButton
