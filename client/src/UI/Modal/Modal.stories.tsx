import { I18nProvider } from "@lingui/react"
import { actions } from "@storybook/addon-actions"
import { withKnobs, boolean, select, text } from "@storybook/addon-knobs"
import { Formik, Form } from "formik"
import React from "react"
import { Button, ButtonType, FormField, Input, Spinner } from ".."
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
    <I18nProvider language="en">
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
    </I18nProvider>
  )
}

export const Complex = () => {
  const title = text("Title", "Complex modal")

  return (
    <I18nProvider language="en">
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
              <Button text="Ok" onClick={button} />
              <Button
                text="Cancel"
                type={ButtonType.SECONDARY}
                onClick={button}
              />
            </ModalFooter>
          </ModalDialog>
        </Modal>
      </RootContainer>
    </I18nProvider>
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
    <I18nProvider language="en">
      <RootContainer>
        <Modal close={close} isOpen={true} resistant={resistant()}>
          <ModalDialog close={close} size={size()} title={title}>
            <Formik<IFormValues>
              initialValues={{ username: "Bob", password: "" }}
              onSubmit={async (_, { setSubmitting }) => {
                setSubmitting(false)
              }}
            >
              {() => (
                <Form>
                  {alert() && (
                    <ModalAlert appearance={alertAppearance()}>
                      Ut malesuada interdum massa in ultrices.
                    </ModalAlert>
                  )}
                  <ModalFormBody>
                    <FormField
                      id="login_username"
                      label="User name or e-mail"
                      name="username"
                      input={<Input disabled={loading} />}
                    />
                    <FormField
                      id="login_password"
                      label="Password"
                      name="password"
                      input={<Input disabled={loading} type="password" />}
                    />
                  </ModalFormBody>
                  <ModalFooter>
                    <Button loading={loading} text={btnText} block />
                  </ModalFooter>
                </Form>
              )}
            </Formik>
          </ModalDialog>
        </Modal>
      </RootContainer>
    </I18nProvider>
  )
}
