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
import * as urls from "../../../urls"
import { ThreadsCategoryModalContext } from "../ThreadsCategoryModalContext"
import CategoryPickerActiveItem from "./MobileCategoryNavActiveCategory"
import MobileCategoryNavCategory from "./MobileCategoryNavCategory"
import MobileCategoryNavLink from "./MobileCategoryNavLink"

const MobileCategoryNavModal: React.FC = () => {
  const categories = React.useContext(CategoriesContext)
  const settings = React.useContext(SettingsContext)
  const { active, isOpen, close } = React.useContext(
    ThreadsCategoryModalContext
  )

  const activeParentId = active ? active.parent.id || active.category.id : null

  return portal(
    <Modal close={close} isOpen={isOpen}>
      <ModalDialog
        close={close}
        size={ModalSize.SMALL}
        title={<Trans id="category_picker.title">Category</Trans>}
      >
        <ModalBody>
          <ClickTrap className="category-picker" onClick={close}>
            <MobileCategoryNavLink
              text={<Trans id="threads.header">All threads</Trans>}
              to={settings?.forumIndexThreads ? urls.index() : urls.threads()}
            />
            {active && <CategoryPickerActiveItem active={active} />}
            {categories.map(
              (category) =>
                category.id !== activeParentId && (
                  <MobileCategoryNavCategory
                    category={category}
                    key={category.id}
                  />
                )
            )}
          </ClickTrap>
        </ModalBody>
      </ModalDialog>
    </Modal>
  )
}

export default MobileCategoryNavModal
