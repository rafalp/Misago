import { t } from "@lingui/macro"
import { I18n } from "@lingui/react"
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
}) => (
  <ModalBody className="category-select-search">
    <div className="row no-gutters">
      <div className="col">
        <I18n>
          {({ i18n }) => (
            <Input
              placeholder={i18n._(
                t("post_thread.search_category")`Search categories`
              )}
              value={search}
              onChange={({ target }) => setSearch(target.value)}
            />
          )}
        </I18n>
      </div>
      {search.trim().length > 0 && (
        <div className="col-auto">
          <ButtonSecondary icon="fas fa-times" onClick={() => setSearch("")} />
        </div>
      )}
    </div>
  </ModalBody>
)

export default PostThreadCategorySelectSearch
