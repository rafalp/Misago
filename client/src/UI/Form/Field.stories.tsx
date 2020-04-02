import { withKnobs, boolean } from "@storybook/addon-knobs"
import React from "react"
import * as Yup from "yup"
import Input from "../Input"
import { CardContainer, RootContainer } from "../Storybook"
import { EmailValidationError } from "../ValidationError"
import Field from "./Field"
import FieldError from "./FieldError"
import Form from "./Form"

export default {
  title: "UI/Form field",
  decorators: [withKnobs],
}

interface IFormValues {
  name: string
  email: string
}

export const FormField = () => {
  const FormSchema = Yup.object().shape({
    email: Yup.string().email("value_error.email"),
  })

  const required = boolean("Required", false)

  const field = (
    <Form<IFormValues>
      id="test_form"
      defaultValues={{
        name: "User",
        email: "invalid@example",
      }}
      disabled={boolean("Disabled", false)}
      validationSchema={FormSchema}
    >
      <Field
        label="Name"
        name="name"
        input={<Input />}
        required={required}
      />
      <Field
        label="E-mail"
        name="email"
        input={<Input invalid={true} type="email" />}
        error={error => (
          <EmailValidationError error={error}>
            {({ message }) => <FieldError>{message}</FieldError>}
          </EmailValidationError>
        )}
        required={required}
      />
    </Form>
  )

  return (
    <>
      <RootContainer padding>{field}</RootContainer>
      <CardContainer padding>{field}</CardContainer>
    </>
  )
}
