import { t } from "@lingui/macro"
import { useLingui } from "@lingui/react"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import Input from "../../../UI/Input"
import { ModalBody } from "../../../UI/Modal"

interface IPostThreadCategorySelectSearchProps {
  search: string
  setSearch: (value: string) => void
}

const PostThreadCategorySelectSearch: React.FC<IPostThreadCategorySelectSearchProps> = ({
  search,
  setSearch,
}) => {
  const { i18n } = useLingui()

  return (
    <ModalBody className="category-select-search">
      <div className="row no-gutters">
        <div className="col">
          <Input
            placeholder={i18n._(
              "post_thread.search_category",
              t`Search categories`
            )}
            value={search}
            onChange={({ target }) => setSearch(target.value)}
          />
        </div>
        {search.trim().length > 0 && (
          <div className="col-auto">
            <ButtonSecondary
              icon="fas fa-times"
              onClick={() => setSearch("")}
            />
          </div>
        )}
      </div>
    </ModalBody>
  )
}

export default PostThreadCategorySelectSearch
