import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select, text } from "@storybook/addon-knobs"
import React from "react"
import { ButtonPrimary, ButtonSecondary } from "../Button"
import { Field, Form, FormFooter } from "../Form"
import Input from "../Input"
import Spinner from "../Spinner"
import { RootContainer } from "../Storybook"
import {
  Modal,
  ModalAlert,
  ModalBody,
  ModalCloseFooter,
  ModalDialog,
  ModalErrorBody,
  ModalFooter,
  ModalFormBody,
  ModalMessageBody,
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
const resistant = () => boolean("Resistant", false)

export const Basic = () => {
  const title = text("Title", "Basic modal")

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
          {alert() && (
            <ModalAlert>Ut malesuada interdum massa in ultrices.</ModalAlert>
          )}
          <ModalBody>
            <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
          </ModalBody>
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}

export const Error = () => {
  const title = text("Title", "Error Modal")
  const footer = boolean("Display footer", false)

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
          <ModalErrorBody header="This content is not available." />
          {footer && <ModalCloseFooter close={close} />}
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}

export const ErrorWithMessage = () => {
  const title = text("Title", "Error Modal")
  const footer = boolean("Display footer", false)

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title={title}>
          <ModalErrorBody
            header="This content is not available."
            message="It may have been moved or deleted, or you are missing permission to see it."
          />
          {footer && <ModalCloseFooter close={close} />}
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}

export const Message = () => {
  const footer = boolean("Display footer", false)

  return (
    <RootContainer>
      <Modal close={close} isOpen={true} resistant={resistant()}>
        <ModalDialog close={close} size={size()} title="Delete thread?">
          <ModalMessageBody
            header="Are you sure you want to delete this thread?"
            message="This action is not reversible."
          />
          {footer && <ModalCloseFooter close={close} />}
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
            <ModalAlert>Ut malesuada interdum massa in ultrices.</ModalAlert>
          )}
          <ModalBody>
            <p className="m-0">Lorem ipsum dolor met sit amet elit.</p>
          </ModalBody>
          <ModalFooter>
            <Spinner small />
            <ButtonSecondary text="Cancel" onClick={button} />
            <ButtonPrimary text="Ok" onClick={button} />
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
              <ModalAlert>Ut malesuada interdum massa in ultrices.</ModalAlert>
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
              <FormFooter
                submitText={btnText}
                loading={loading}
                onCancel={close}
              />
            </ModalFooter>
          </Form>
        </ModalDialog>
      </Modal>
    </RootContainer>
  )
}

export const WithFormAlt = () => {
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
              <ModalAlert>Ut malesuada interdum massa in ultrices.</ModalAlert>
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
