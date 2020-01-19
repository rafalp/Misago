import { useMutation } from "@apollo/react-hooks"
import { Trans } from "@lingui/macro"
import { gql } from "apollo-boost"
import { Formik, Form } from "formik"
import React from "react"
import {
  Button,
  ButtonType,
  RootError,
  FormField,
  Input,
  ModalAlert,
  ModalDialog,
  ModalFooter,
  ModalFormBody,
  ModalHeader,
} from "../UI"
import { useAuth } from "../auth"
import { IMutationError } from "../types"

const LOGIN = gql`
  mutation Login($username: String!, $password: String!) {
    login(username: $username, password: $password) {
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

interface ILoginData {
  login: {
    errors: Array<IMutationError> | null
    user: {
      id: string
      name: string
    } | null
    token: string | null
  }
}

interface ILoginValues {
  username: string
  password: string
}

interface ILoginModalProps {
  close: () => void
  showRegister: () => void
}

const LoginModal: React.FC<ILoginModalProps> = ({ close, showRegister }) => {
  const { login } = useAuth()
  const [error, setError] = React.useState<string | null>(null)
  const [authenticate, { data, error: graphqlError }] = useMutation<
    ILoginData,
    ILoginValues
  >(LOGIN, { errorPolicy: "all" })

  return (
    <ModalDialog className="modal-dialog-auth modal-dialog-login" size="small">
      <ModalHeader
        title={<Trans id="login.title">Log in</Trans>}
        close={close}
      />
      <Formik<ILoginValues>
        initialValues={{ username: "", password: "" }}
        onSubmit={async (variables, { setSubmitting }) => {
          const { username, password } = variables
          if (!username.trim().length || !password.length) {
            setError("value_error.all_fields_are_required")
            setSubmitting(false)
            return false
          }

          setError(null)

          const data = await authenticate({ variables })
          const { user, token } = data.data?.login || {}
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
              dataErrors={data?.login.errors}
              plainError={error}
              messages={{
                "value_error.all_fields_are_required": (
                  <Trans>Fill out all fields.</Trans>
                ),
                "value_error.invalid_credentials": (
                  <Trans>Login or password is incorrect.</Trans>
                ),
              }}
            >
              {({ message }) => <ModalAlert>{message}</ModalAlert>}
            </RootError>
            <ModalFormBody>
              <FormField
                id="login_username"
                label={
                  <Trans id="login.input.username">User name or e-mail</Trans>
                }
                name="username"
                input={<Input maxLength={255} />}
              />
              <FormField
                id="login_password"
                label={<Trans id="login.input.password">Password</Trans>}
                name="password"
                input={<Input maxLength={255} type="password" />}
              />
            </ModalFormBody>
            <ModalFooter>
              <Button
                disabled={isSubmitting}
                text={<Trans id="login.submit">Log in</Trans>}
                block
              />
              <Button
                disabled={isSubmitting}
                text={
                  <Trans id="login.register">
                    Not a member? <strong>Sign up</strong>
                  </Trans>
                }
                type={ButtonType.LINK}
                block
                onClick={showRegister}
              />
            </ModalFooter>
          </Form>
        )}
      </Formik>
    </ModalDialog>
  )
}

export default LoginModal
