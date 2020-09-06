import { Trans } from "@lingui/macro"
import React from "react"
import { useModalContext } from "../../../Context"
import { Modal, ModalBody, ModalDialog } from "../../../UI/Modal"
import { ICategoryChoice } from "../PostThread.types"

interface IPostThreadCategorySelectProps {
  choices: Array<ICategoryChoice>
  setValue: (value: string) => void
}

const PostThreadCategorySelect: React.FC<IPostThreadCategorySelectProps> = ({
  choices,
  setValue,
}) => {
  const { isOpen, closeModal } = useModalContext()
  return (
    <Modal isOpen={isOpen} close={closeModal}>
      <ModalDialog
        title={
          <Trans id="post_thread.select_category">Select a category</Trans>
        }
        close={closeModal}
      >
        <ModalBody>
          {choices.map((category) => (
            <React.Fragment key={category.id}>
              <div className="mb-3">
                <button
                  className="btn btn-secondary w-100 text-left mb-3"
                  type="button"
                  onClick={() => {
                    setValue(category.id)
                    closeModal()
                  }}
                >
                  {category.name}
                </button>
                {category.children.map((child) => (
                  <div className="pl-3 mb-3" key={child.id}>
                    <button
                      className="btn btn-secondary w-100 text-left"
                      type="button"
                      onClick={() => {
                        setValue(child.id)
                        closeModal()
                      }}
                    >
                      {child.name}
                    </button>
                  </div>
                ))}
              </div>
            </React.Fragment>
          ))}
        </ModalBody>
      </ModalDialog>
    </Modal>
  )
}

export default PostThreadCategorySelect
