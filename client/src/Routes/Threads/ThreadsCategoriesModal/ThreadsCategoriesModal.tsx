import { Trans } from "@lingui/macro"
import React from "react"
import { useCategoriesContext, useSettingsContext } from "../../../Context"
import ClickTrap from "../../../UI/ClickTrap"
import { Modal, ModalBody, ModalDialog, ModalSize } from "../../../UI/Modal"
import portal from "../../../UI/portal"
import * as urls from "../../../urls"
import ThreadsCategoriesModalActiveItem from "./ThreadsCategoriesModalActiveItem"
import { useThreadsCategoriesModalContext } from "./ThreadsCategoriesModalContext"
import ThreadsCategoriesModalItem from "./ThreadsCategoriesModalItem"
import ThreadsCategoriesModalLink from "./ThreadsCategoriesModalLink"

const ThreadsCategoriesModal: React.FC = () => {
  const categories = useCategoriesContext()
  const settings = useSettingsContext()
  const { active, isOpen, close } = useThreadsCategoriesModalContext()

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
            <ThreadsCategoriesModalLink
              text={<Trans id="threads.header">All threads</Trans>}
              to={settings.forumIndexThreads ? urls.index() : urls.threads()}
            />
            {active && <ThreadsCategoriesModalActiveItem active={active} />}
            {categories.map(
              (category) =>
                category.id !== activeParentId && (
                  <ThreadsCategoriesModalItem
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

export default ThreadsCategoriesModal
