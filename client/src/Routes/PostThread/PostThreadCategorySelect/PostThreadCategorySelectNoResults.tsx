import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { ModalMessageBody } from "../../../UI/Modal"

interface PostThreadCategorySelectNoResultsProps {
  setSearch: (value: string) => void
}

const PostThreadCategorySelectNoResults: React.FC<PostThreadCategorySelectNoResultsProps> = ({
  setSearch,
}) => (
  <ModalMessageBody
    header={
      <Trans id="post_thread.category_search_empty">
        No categories matching search have been found.
      </Trans>
    }
    actions={
      <ButtonSecondary
        text={
          <Trans id="post_thread.category_search_clear">Clear search</Trans>
        }
        responsive
        onClick={() => setSearch("")}
      />
    }
  />
)

export default PostThreadCategorySelectNoResults
