import { Trans } from "@lingui/macro"
import React from "react"

interface IPostThreadCategoryInputEmptyProps {
  disabled?: boolean
  onClick: () => void
}

const PostThreadCategoryInputEmpty: React.FC<IPostThreadCategoryInputEmptyProps> = ({
  disabled,
  onClick,
}) => (
  <button
    className="btn btn-secondary btn-responsive"
    type="button"
    disabled={disabled}
    onClick={onClick}
  >
    <Trans id="post_thread.select_category">Select a category</Trans>
  </button>
)

export default PostThreadCategoryInputEmpty
