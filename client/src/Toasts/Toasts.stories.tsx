import { action } from "@storybook/addon-actions"
import React from "react"
import { ToastsContext, ToastsContextProvider } from "../Context"
import { ButtonPrimary, Form, Field, Input } from "../UI"
import { RootContainer } from "../UI/Storybook"
import Toast from "./Toast"
import Toasts from "./Toasts"
import ToastsContainer from "./ToastsContainer"

export default {
  title: "Toasts",
}

const remove = action("remove toast")

export const Static = () => (
  <ToastsContainer>
    <Toast
      text="Hello, world! This is a toast message."
      remove={remove}
      show
    />
    <Toast
      text="At vero eos et accusamus et iusto odio dignissimos ducimus qui blanditiis praesentium voluptatum deleniti."
      remove={remove}
      show
    />
  </ToastsContainer>
)

interface IFormValues {
  text: string
}

export const Dynamic = () => (
  <ToastsContextProvider>
    <Toasts />
    <RootContainer padding>
      <ToastsContext.Consumer>
        {({ showToast }) => (
          <Form<IFormValues>
            id="toasts_test_form"
            defaultValues={{ text: "Hello world!" }}
            onSubmit={({ data: { text } }) => {
              if (text) showToast(text)
            }}
          >
            <Field label="Toast text" name="text" input={<Input />} />
            <ButtonPrimary text="Open toast" />
          </Form>
        )}
      </ToastsContext.Consumer>
    </RootContainer>
  </ToastsContextProvider>
)
