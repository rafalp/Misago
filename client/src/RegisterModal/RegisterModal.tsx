import { useMutation } from "@apollo/react-hooks"
import { Plural, Trans } from "@lingui/macro"
import { gql } from "apollo-boost"
import { Formik, Form } from "formik"
import React from "react"
import ReactDOM from "react-dom"
import * as Yup from "yup"
import { Button, FieldError, Modal, ModalBody, ModalFooter, Spinner } from "../UI"
import root from "../modalsRoot"
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
  isOpen: boolean
  settings: ISettings | null
  closeModal: () => void
}

const RegisterModal: React.FC<IRegisterModalProps> = ({ isOpen, settings, closeModal }) => {
  const [register] = useMutation<IRegisterData, IRegisterInput>(REGISTER)

  if (!settings || !root) return null

  const RegisterSchema = Yup.object().shape({
    name: Yup.string()
      .required("value_error.missing")
      .min(settings.usernameMinLength, "value_error.any_str.min_length")
      .max(settings.usernameMaxLength, "value_error.any_str.max_length"),
    password: Yup.string()
      .required("value_error.missing")
      .min(settings.passwordMinLength, "value_error.any_str.min_length")
      .max(settings.passwordMaxLength, "value_error.any_str.max_length"),
    email: Yup.string()
      .required("value_error.missing")
      .email("value_error.email"),
  })

  return ReactDOM.createPortal(
    <Modal
      className="modal-register"
      close={closeModal}
      isOpen={isOpen}
      title={<Trans id="register.title">Register</Trans>}
      resistant
    >
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
        {({ values, errors, handleChange, isSubmitting }) => (
          <Form>
            <ModalBody>
              <div className="form-group">
                Name
                <input
                  className="form-control"
                  type="text"
                  name="name"
                  onChange={handleChange}
                  value={values.name}
                />
                <FieldError
                  error={errors.name}
                  messages={{
                    "value_error.missing": <Trans>Enter your name.</Trans>,
                    "value_error.any_str.min_length": (
                      <Plural
                        value={settings.usernameMinLength}
                        one={
                          <Trans>
                            Name should be at least # character long (it has {values.name.length}).
                          </Trans>
                        }
                        other={
                          <Trans>
                            Name should be at least # characters long (it has {values.name.length}).
                          </Trans>
                        }
                      />
                    ),
                    "value_error.any_str.max_length": (
                      <Plural
                        value={settings.usernameMaxLength}
                        one={
                          <Trans>
                            Name should be at least # character long (it has {values.name.length}).
                          </Trans>
                        }
                        other={
                          <Trans>
                            Name should be at least # characters long (it has {values.name.length}).
                          </Trans>
                        }
                      />
                    ),
                  }}
                />
              </div>
              <div className="form-group">
                E-mail
                <input
                  className="form-control"
                  type="email"
                  name="email"
                  onChange={handleChange}
                  value={values.email}
                />
                <FieldError error={errors.email} messages={{}} />
              </div>
              <div className="form-group">
                Password
                <input
                  className="form-control"
                  type="password"
                  name="password"
                  onChange={handleChange}
                  value={values.password}
                />
                <FieldError
                  error={errors.password}
                  messages={{
                    "value_error.missing": <Trans>Enter password.</Trans>,
                    "value_error.any_str.min_length": (
                      <Plural
                        value={settings.passwordMinLength}
                        one={
                          <Trans>
                            Password should be at least # character long (it has{" "}
                            {values.password.length}).
                          </Trans>
                        }
                        other={
                          <Trans>
                            Password should be at least # characters long (it has{" "}
                            {values.password.length}).
                          </Trans>
                        }
                      />
                    ),
                    "value_error.any_str.max_length": (
                      <Plural
                        value={settings.passwordMaxLength}
                        one={
                          <Trans>
                            Password should be at least # character long (it has{" "}
                            {values.password.length}).
                          </Trans>
                        }
                        other={
                          <Trans>
                            Password should be at least # characters long (it has{" "}
                            {values.password.length}).
                          </Trans>
                        }
                      />
                    ),
                  }}
                />
              </div>
            </ModalBody>
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
    </Modal>,
    root
  )
}

export default RegisterModal
