import { useMutation } from "@apollo/react-hooks"
import { Trans } from "@lingui/macro"
import { gql } from "apollo-boost"
import { Formik, Form } from "formik"
import React from "react"
import * as Yup from "yup"
import {
  Button,
  RootError,
  EmailValidationError,
  FieldError,
  FormField,
  Input,
  ModalAlert,
  ModalFooter,
  ModalFormBody,
  ModalHeader,
  PasswordValidationError,
  Spinner,
  UsernameValidationError,
} from "../UI"
import { IMutationError, ISettings } from "../types"

const REGISTER = gql`
  mutation Register($input: RegisterInput!) {
    register(input: $input) {
      errors {
        location
        message
        type
      }
      user {
        id
        name
      }
      token
    }
  }
`

interface IRegisterData {
  register: {
    errors: Array<IMutationError> | null
    user: {
      id: string
      name: string
    } | null
    token: string | null
  }
}

interface IRegisterValues {
  name: string
  email: string
  password: string
}

interface IRegisterInput {
  input: IRegisterValues
}

interface IRegisterModalProps {
  settings: ISettings
  closeModal: () => void
}

const RegisterModal: React.FC<IRegisterModalProps> = ({ settings, closeModal }) => {
  const [register, { data, error: graphqlError }] = useMutation<IRegisterData, IRegisterInput>(
    REGISTER,
    { errorPolicy: "all" }
  )

  const RegisterSchema = Yup.object().shape({
    name: Yup.string()
      .required("value_error.missing")
      .min(settings.usernameMinLength, "value_error.any_str.min_length")
      .max(settings.usernameMaxLength, "value_error.any_str.max_length")
      .matches(/^[a-zA-Z0-9]+$/, "value_error.username"),
    password: Yup.string()
      .required("value_error.missing")
      .min(settings.passwordMinLength, "value_error.any_str.min_length")
      .max(settings.passwordMaxLength, "value_error.any_str.max_length"),
    email: Yup.string()
      .required("value_error.missing")
      .email("value_error.email"),
  })

  return (
    <>
      <ModalHeader title={<Trans id="register.title">Register</Trans>} close={closeModal} />
      <Formik<IRegisterValues>
        initialValues={{ name: "", email: "", password: "" }}
        validationSchema={RegisterSchema}
        onSubmit={async (input, { setFieldError, setSubmitting }) => {
          const data = await register({ variables: { input } })
          const errors = data.data?.register?.errors
          errors?.forEach(({ location, type }) => {
            const field = location.join(".")
            setFieldError(field, type)
          })
          setSubmitting(false)
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <RootError graphqlError={graphqlError} dataErrors={data?.register.errors}>
              {({ message }) => <ModalAlert>{message}</ModalAlert>}
            </RootError>
            <ModalFormBody>
              <FormField
                id="register_name"
                label={<Trans>User name:</Trans>}
                name="name"
                input={<Input maxLength={settings.usernameMaxLength} />}
                error={(error, value) => (
                  <UsernameValidationError
                    error={error}
                    value={value.trim().length}
                    min={settings.usernameMinLength}
                    max={settings.usernameMaxLength}
                  >
                    {({ message }) => <FieldError>{message}</FieldError>}
                  </UsernameValidationError>
                )}
              />
              <FormField
                id="register_email"
                label={<Trans>E-mail:</Trans>}
                name="email"
                input={<Input maxLength={100} type="email" />}
                error={error => (
                  <EmailValidationError error={error}>
                    {({ message }) => <FieldError>{message}</FieldError>}
                  </EmailValidationError>
                )}
              />
              <FormField
                id="register_password"
                label={<Trans>Password:</Trans>}
                name="password"
                input={<Input maxLength={settings.passwordMaxLength} type="password" />}
                error={(error, value) => (
                  <PasswordValidationError
                    error={error}
                    value={value.length}
                    min={settings.passwordMinLength}
                    max={settings.passwordMaxLength}
                  >
                    {({ message }) => <FieldError>{message}</FieldError>}
                  </PasswordValidationError>
                )}
              />
            </ModalFormBody>
            <ModalFooter>
              {isSubmitting && <Spinner small />}
              <Button
                disabled={isSubmitting}
                text={<Trans id="register.submit">Register account</Trans>}
              />
            </ModalFooter>
          </Form>
        )}
      </Formik>
    </>
  )
}

export default RegisterModal
