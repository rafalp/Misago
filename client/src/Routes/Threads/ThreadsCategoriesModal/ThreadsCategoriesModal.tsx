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
import ThreadsCategoriesModalActiveItem from "./ThreadsCategoriesModalActiveItem"
import { ThreadsCategoriesModalContext } from "./ThreadsCategoriesModalContext"
import ThreadsCategoriesModalItem from "./ThreadsCategoriesModalItem"
import ThreadsCategoriesModalLink from "./ThreadsCategoriesModalLink"

const ThreadsCategoriesModal: React.FC = () => {
  const categories = React.useContext(CategoriesContext)
  const settings = React.useContext(SettingsContext)
  const { active, isOpen, close } = React.useContext(
    ThreadsCategoriesModalContext
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
            <ThreadsCategoriesModalLink
              text={<Trans id="threads.header">All threads</Trans>}
              to={settings?.forumIndexThreads ? urls.index() : urls.threads()}
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
