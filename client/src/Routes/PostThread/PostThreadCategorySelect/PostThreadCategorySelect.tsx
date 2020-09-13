import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalDialog } from "../../../UI/Modal"
import { ICategoryChoice } from "../PostThread.types"
import PostThreadCategorySelectItems from "./PostThreadCategorySelectItems"
import PostThreadCategorySelectNoResults from "./PostThreadCategorySelectNoResults"
import PostThreadCategorySelectSearch from "./PostThreadCategorySelectSearch"
import useFilteredChoices from "./useFilteredChoices"

interface IPostThreadCategorySelectProps {
  choices: Array<ICategoryChoice>
  validChoices: Array<string>
  setValue: (value: string) => void
}

const PostThreadCategorySelect: React.FC<IPostThreadCategorySelectProps> = ({
  choices,
  validChoices,
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
        <PostThreadCategorySelectSearch
          search={search}
          setSearch={setSearch}
        />
        {filteredChoices.length > 0 ? (
          <PostThreadCategorySelectItems
            choices={filteredChoices}
            validChoices={validChoices}
            setValue={(category: string) => {
              setValue(category)
              closeModal()
            }}
          />
        ) : (
          <PostThreadCategorySelectNoResults setSearch={setSearch} />
        )}
      </ModalDialog>
    </Modal>
  )
}

export default PostThreadCategorySelect
