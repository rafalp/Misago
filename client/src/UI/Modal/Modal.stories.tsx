import { I18nProvider } from "@lingui/react"
import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select } from "@storybook/addon-knobs"
import React from "react"
import { Button, ButtonType, Spinner } from ".."
import { RootContainer } from "../Storybook"
import {
  Modal,
  ModalAlert,
  ModalBody,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
} from "."

export default {
  title: "UI/Modal",
  decorators: [withKnobs],
}

const { close, button } = actions({
  close: "close modal",
  button: "click button",
})

const size = () =>
  select(
    "Size",
    {
      Default: "default",
      Small: "small",
      Large: "large",
      "Extra large": "extra_large",
    },
    "default"
  )
const alert = () => boolean("Display alert", false)
const alertAppearance = () =>
  select(
    "Alert appearance",
    {
      Primary: "primary",
      Secondary: "secondary",
      Success: "success",
      Danger: "danger",
      Warning: "warning",
      Info: "info",
    },
    "danger"
  )
const resistant = () => boolean("Resistant", false)

export const Basic = () => {
  return (
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()}>
          <ModalDialog close={close} size={size()} title="Basic modal">
            {alert() && (
              <ModalAlert appearance={alertAppearance()}>
                Ut malesuada interdum massa in ultrices.
              </ModalAlert>
            )}
            <ModalBody>
              <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
            </ModalBody>
          </ModalDialog>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}

export const Complex = () => {
  return (
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()}>
          <ModalDialog close={close} size={size()} title="Complex modal">
            {alert() && (
              <ModalAlert appearance={alertAppearance()}>
                Ut malesuada interdum massa in ultrices.
              </ModalAlert>
            )}
            <ModalBody>
              <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
            </ModalBody>
            <ModalFooter>
              <Spinner small />
              <Button text="Ok" onClick={button} />
              <Button text="Cancel" type={ButtonType.SECONDARY} onClick={button} />
            </ModalFooter>
          </ModalDialog>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}

export const Form = () => {
  return (
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()}>
          <ModalDialog close={close} size={size()} title="Form modal">
            {alert() && (
              <ModalAlert appearance={alertAppearance()}>
                Ut malesuada interdum massa in ultrices.
              </ModalAlert>
            )}
            <ModalFormBody>Here</ModalFormBody>
            <ModalFooter>
              <Spinner small />
              <Button text="Ok" onClick={button} />
              <Button text="Cancel" type={ButtonType.SECONDARY} onClick={button} />
            </ModalFooter>
          </ModalDialog>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}
