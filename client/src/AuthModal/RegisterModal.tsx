import { useMutation } from "@apollo/react-hooks"
import { Trans } from "@lingui/macro"
import { gql } from "apollo-boost"
import { Formik, Form } from "formik"
import React from "react"
import * as Yup from "yup"
import {
  Button,
  ButtonType,
  RootError,
  EmailValidationError,
  FieldError,
  FormField,
  Input,
  ModalAlert,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
  ModalHeader,
  ModalSize,
  PasswordValidationError,
  UsernameValidationError,
} from "../UI"
import { useAuth } from "../auth"
import { IMutationError } from "../types"

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

interface ISettings {
  passwordMinLength: number
  passwordMaxLength: number
  usernameMinLength: number
  usernameMaxLength: number
}

interface IRegisterModalProps {
  settings: ISettings
  close: () => void
  showLogin: () => void
}

const RegisterModal: React.FC<IRegisterModalProps> = ({
  settings,
  close,
  showLogin,
}) => {
  const { login } = useAuth()
  const [register, { data, error: graphqlError }] = useMutation<
    IRegisterData,
    IRegisterInput
  >(REGISTER, { errorPolicy: "all" })

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
    <ModalDialog
      className="modal-dialog-auth modal-dialog-register"
      size={ModalSize.SMALL}
    >
      <ModalHeader
        title={<Trans id="register.title">Sign up</Trans>}
        close={close}
      />
      <Formik<IRegisterValues>
        initialValues={{ name: "", email: "", password: "" }}
        validationSchema={RegisterSchema}
        onSubmit={async (input, { setFieldError, setSubmitting }) => {
          const data = await register({ variables: { input } })
          const { errors, token, user } = data.data?.register || {}
          setSubmitting(false)

          errors?.forEach(({ location, type }) => {
            const field = location.join(".")
            setFieldError(field, type)
          })

          if (token && user) {
            login(token, user)
            close()
          }
        }}
      >
        {({ isSubmitting }) => (
          <Form>
            <RootError
              graphqlError={graphqlError}
              dataErrors={data?.register.errors}
            >
              {({ message }) => <ModalAlert>{message}</ModalAlert>}
            </RootError>
            <ModalFormBody>
              <FormField
                id="register_name"
                label={<Trans id="input.name">User name</Trans>}
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
                label={<Trans id="input.email">E-mail</Trans>}
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
                label={<Trans id="input.password">Password</Trans>}
                name="password"
                input={
                  <Input
                    maxLength={settings.passwordMaxLength}
                    type="password"
                  />
                }
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
              <Button
                loading={isSubmitting}
                text={
                  isSubmitting ? (
                    <Trans id="register.submitting">Signing up...</Trans>
                  ) : (
                    <Trans id="register.submit">Sign up</Trans>
                  )
                }
                block
              />
              <Button
                disabled={isSubmitting}
                text={
                  <Trans id="register.login">
                    Already a member? <strong>Log in</strong>
                  </Trans>
                }
                type={ButtonType.LINK}
                block
                onClick={showLogin}
              />
            </ModalFooter>
          </Form>
        )}
      </Formik>
    </ModalDialog>
  )
}

export default RegisterModal
