import { Trans } from "@lingui/macro"
import React from "react"

const PostThreadCategoryInputPlaceholder: React.FC = () => (
  <span className="form-control-category-select-placeholder">
    <Trans id="post_thread.select_category">Select a category</Trans>
  </span>
)

export default PostThreadCategoryInputPlaceholder
