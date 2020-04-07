import { Trans } from "@lingui/macro"
import React from "react"
import { CategoriesContext, SettingsContext } from "../../../Context"
import {
  ClickTrap,
  Modal,
  ModalBody,
  ModalDialog,
  ModalSize,
  portal,
} from "../../../UI"
import CategoryPickerActiveItem from "./CategoryPickerActiveItem"
import CategoryPickerCategory from "./CategoryPickerCategory"
import CategoryPickerItem from "./CategoryPickerItem"

interface ICategoryPickerModalProps {
  active?: { id: string } | null
  isOpen: boolean
  close: () => void
}

const CategoryPickerModal: React.FC<ICategoryPickerModalProps> = ({
  active,
  close,
  isOpen,
}) => {
  const categories = React.useContext(CategoriesContext)
  const { forumIndexThreads } = React.useContext(SettingsContext) || {
    forumIndexThreads: true,
  }

  return portal(
    <Modal close={close} isOpen={isOpen}>
      <ModalDialog
        close={close}
        size={ModalSize.SMALL}
        title={<Trans id="category_picker.title">Category</Trans>}
      >
        <ModalBody>
          <ClickTrap className="category-picker" onClick={close}>
            <CategoryPickerItem
              text={<Trans id="threads.header">All threads</Trans>}
              to={forumIndexThreads ? "/" : "/threads/"}
            />
            {active && <CategoryPickerActiveItem active={active} />}
            {categories.map((category) => (
              <CategoryPickerCategory category={category} key={category.id} />
            ))}
          </ClickTrap>
        </ModalBody>
      </ModalDialog>
    </Modal>
  )
}

export default CategoryPickerModal
