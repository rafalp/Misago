import { withKnobs, boolean } from "@storybook/addon-knobs"
import { actions } from "@storybook/addon-actions"
import React from "react"
import * as Yup from "yup"
import { Card, CardBody, CardFooter } from "../Card"
import Input from "../Input"
import Select from "../Select"
import { CardContainer, RootContainer } from "../Storybook"
import { EmailValidationError } from "../ValidationError"
import { Field, FieldError, Form, FormFooter } from "."

export default {
  title: "UI/Form",
  decorators: [withKnobs],
}

interface IFormValues {
  name: string
  email: string
  color: string
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
        color: "blue",
      }}
      disabled={boolean("Disabled", false)}
      validationSchema={FormSchema}
    >
      <Field label="Name" name="name" input={<Input />} required={required} />
      <Field
        label="E-mail"
        name="email"
        input={<Input invalid={true} type="email" />}
        error={(error) => (
          <EmailValidationError error={error}>
            {({ message }) => <FieldError>{message}</FieldError>}
          </EmailValidationError>
        )}
        required={required}
      />
      <Field
        label="Favorite color"
        name="color"
        input={
          <Select
            options={[
              { value: "blue", name: "Blue" },
              { value: "red", name: "Red" },
              { value: "green", name: "Green" },
            ]}
          />
        }
        required={required}
      />
    </Form>
  )

  return (
    <>
      <RootContainer>{field}</RootContainer>
      <CardContainer>{field}</CardContainer>
    </>
  )
}

const { cancel, submit } = actions({
  cancel: "canceled",
  submit: "submitted",
})

export const Footer = () => {
  const danger = boolean("Danger", false)
  const disabled = boolean("Disabled", false)
  const loading = boolean("Loading", false)

  return (
    <RootContainer>
      <Card>
        <form
          onSubmit={(event) => {
            event.preventDefault()
            submit(event)
          }}
        >
          <CardBody>Example card with form</CardBody>
          <CardFooter>
            <FormFooter
              submitText="Submit"
              danger={danger}
              disabled={disabled}
              loading={loading}
              onCancel={cancel}
            />
          </CardFooter>
        </form>
      </Card>
    </RootContainer>
  )
}
