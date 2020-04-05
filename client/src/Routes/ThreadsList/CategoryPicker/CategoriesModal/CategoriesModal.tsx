import { Trans } from "@lingui/macro"
import React from "react"
import { Link } from "react-router-dom"
import { CategoriesContext, SettingsContext } from "../../../../Context"
import { Modal, ModalBody, ModalDialog, portal } from "../../../../UI"
import * as urls from "../../../../urls"

interface ICategoriesModalProps {
  isOpen: boolean
  close: () => void
}

const CategoriesModal: React.FC<ICategoriesModalProps> = ({
  close,
  isOpen,
}) => {
  const categories = React.useContext(CategoriesContext)
  const settings = React.useContext(SettingsContext) || {
    forumIndexThreads: true,
  }

  return portal(
    <Modal close={close} isOpen={isOpen}>
      <ModalDialog
        close={close}
        title={<Trans id="categories_modal.title">Go to category</Trans>}
      >
        <ModalBody>
          {categories.map((category) => (
            <div key={category.id}>
              <Link to={urls.category(category)}>
                {category.name}
              </Link>
            </div>
          ))}
        </ModalBody>
      </ModalDialog>
    </Modal>
  )
}

export default CategoriesModal
