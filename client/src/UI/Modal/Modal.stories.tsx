import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select, text } from "@storybook/addon-knobs"
import React from "react"
import {
  ButtonPrimary,
  ButtonSecondary,
  Field,
  Form,
  Input,
  Spinner,
} from ".."
import { RootContainer } from "../Storybook"
import {
  Modal,
  ModalAlert,
  ModalBody,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
  ModalSize,
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
      Default: ModalSize.DEFAULT,
      Small: ModalSize.SMALL,
      Large: ModalSize.LARGE,
      "Extra large": ModalSize.EXTRA_LARGE,
    },
    ModalSize.DEFAULT
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
  const title = text("Title", "Basic modal")

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
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
  )
}

export const Complex = () => {
  const title = text("Title", "Complex modal")

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
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
            <ButtonPrimary text="Ok" onClick={button} />
            <ButtonSecondary text="Cancel" onClick={button} />
          </ModalFooter>
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}

interface IFormValues {
  username: string
  password: string
}

export const WithForm = () => {
  const title = text("Title", "Form modal")
  const btnText = text("Button text", "Submit")
  const loading = boolean("Loading", false)

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
          <Form<IFormValues>
            id="modal_form"
            defaultValues={{ username: "Bob", password: "" }}
            onSubmit={async () => {}}
          >
            {alert() && (
              <ModalAlert appearance={alertAppearance()}>
                Ut malesuada interdum massa in ultrices.
              </ModalAlert>
            )}
            <ModalFormBody>
              <Field
                label="User name or e-mail"
                name="username"
                input={<Input disabled={loading} />}
              />
              <Field
                label="Password"
                name="password"
                input={<Input disabled={loading} type="password" />}
              />
            </ModalFormBody>
            <ModalFooter>
              <ButtonPrimary loading={loading} text={btnText} block />
            </ModalFooter>
          </Form>
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}
