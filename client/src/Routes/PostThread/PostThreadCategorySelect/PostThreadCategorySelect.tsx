import { Trans, t } from "@lingui/macro"
import { I18n } from "@lingui/react"
import React from "react"
import { useModalContext } from "../../../Context"
import { ButtonSecondary } from "../../../UI/Button"
import CategoryIcon from "../../../UI/CategoryIcon"
import Input from "../../../UI/Input"
import { Modal, ModalBody, ModalDialog } from "../../../UI/Modal"
import { ICategoryChoice } from "../PostThread.types"
import useFilteredChoices from "./useFilteredChoices"

interface IPostThreadCategorySelectProps {
  choices: Array<ICategoryChoice>
  setValue: (value: string) => void
}

const PostThreadCategorySelect: React.FC<IPostThreadCategorySelectProps> = ({
  choices,
  setValue,
}) => {
  const { closeModal, isOpen } = useModalContext()
  const [search, setSearch] = React.useState<string>("")
  const filteredChoices = useFilteredChoices(choices, search)

  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={
          <Trans id="post_thread.select_category">Select a category</Trans>
        }
        close={closeModal}
      >
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
              <div className="col-auto pl-3">
                <ButtonSecondary
                  icon="fas fa-times"
                  onClick={() => setSearch("")}
                />
              </div>
            )}
          </div>
        </ModalBody>
        <ModalBody className="category-select">
          {filteredChoices.map((category) => (
            <React.Fragment key={category.id}>
              <button
                className="btn btn-secondary btn-sm w-100 text-left mb-2"
                type="button"
                onClick={() => {
                  setValue(category.id)
                  closeModal()
                }}
              >
                <CategoryIcon category={category} />
                <span>{category.name}</span>
              </button>
              {category.children.map((child) => (
                <div className="pl-3 mb-2" key={child.id}>
                  <button
                    className="btn btn-secondary btn-sm w-100 text-left"
                    type="button"
                    onClick={() => {
                      setValue(child.id)
                      closeModal()
                    }}
                  >
                    <CategoryIcon category={child} />
                    <span>{child.name}</span>
                  </button>
                </div>
              ))}
            </React.Fragment>
          ))}
        </ModalBody>
      </ModalDialog>
    </Modal>
  )
}

export default PostThreadCategorySelect
