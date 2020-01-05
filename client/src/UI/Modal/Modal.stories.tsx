import { I18nProvider } from "@lingui/react"
import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select } from "@storybook/addon-knobs"
import React from "react"
import { Button, Spinner } from ".."
import { RootContainer } from "../Storybook"
import { Modal, ModalBody, ModalFooter, ModalSize } from "."

export default {
  title: "UI/Modal",
  decorators: [withKnobs],
}

const { close, button } = actions({ close: "close modal", button: "click button" })

const size = () => select(
  "Size",
  {
    Default: ModalSize.DEFAULT,
    Small: ModalSize.SMALL,
    Large: ModalSize.LARGE,
    "Extra large": ModalSize.EXTRA_LARGE,
  },
  ModalSize.DEFAULT
)
const resistant = () => boolean(
  "Resistant", false
)

export const Basic = () => {
  return (
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()} size={size()} title="Basic modal">
          <ModalBody>
            <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
          </ModalBody>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}

export const Complex = () => {
  return (
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()} size={size()} title="Basic modal">
          <ModalBody>
            <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
          </ModalBody>
          <ModalFooter>
            <Spinner small />
            <Button text="Ok" type="primary" onClick={button} />
            <Button text="Cancel" type="secondary" onClick={button} />
          </ModalFooter>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}
