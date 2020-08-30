import { Trans } from "@lingui/macro"
import React from "react"
import { Redirect } from "react-router-dom"
import * as Yup from "yup"
import { useToastsContext } from "../../Context"
import {
  Card,
  CardAlert,
  CardFooter,
  CardFormBody,
  CardHeader,
} from "../../UI/Card"
import { Field, FieldError, Form, FormFooter } from "../../UI/Form"
import Input from "../../UI/Input"
import RootError from "../../UI/RootError"
import {
  CategoryValidationError,
  ThreadTitleValidationError,
  ValidationError,
} from "../../UI/ValidationError"
import * as urls from "../../urls"
import { ICategoryChoice } from "./PostThread.types"
import usePostThreadMutation from "./usePostThreadMutation"

const Editor = React.lazy(() => import("../../Editor"))

interface IPostThreadFormProps {
  categories: Array<ICategoryChoice>
}

interface IPostThreadFormValues {
  category: string
  title: string
  body: string
}

const PostThreadForm: React.FC<IPostThreadFormProps> = ({ categories }) => {
  const { showToast } = useToastsContext()
  const [
    postThread,
    { data, loading, error: graphqlError },
  ] = usePostThreadMutation()

  const PostThreadSchema = Yup.object().shape({
    category: Yup.string().required("value_error.missing"),
    title: Yup.string()
      .required("value_error.thread_title.missing")
      .min(2, "value_error.any_str.min_length")
      .max(200, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
    body: Yup.string()
      .required("value_error.missing")
      .min(1, "value_error.any_str.min_length")
      .max(2000, "value_error.any_str.max_length"),
  })

  if (data?.postThread.thread) {
    return <Redirect to={urls.thread(data.postThread.thread)} />
  }

  return (
    <Card>
      <CardHeader
        title={<Trans id="post_thread.form">Post a new thread</Trans>}
      />
      <Form<IPostThreadFormValues>
        defaultValues={{
          category: "",
          title: "",
          body: "",
        }}
        disabled={loading}
        validationSchema={PostThreadSchema}
        onSubmit={async ({ clearError, setError, data: input }) => {
          clearError()

          const result = await postThread({ variables: { input } })
          const { errors, thread } = result.data?.postThread || {}

          errors?.forEach(({ location, type, message }) => {
            const field = location.join(".")
            console.log(field)
            setError(field, type, message)
          })

          if (thread) {
            showToast(
              <Trans id="post_thread.message">
                New thread has been posted.
              </Trans>
            )
          }
        }}
      >
        <RootError
          graphqlError={graphqlError}
          dataErrors={data?.postThread.errors}
        >
          {({ message }) => <CardAlert>{message}</CardAlert>}
        </RootError>
        <CardFormBody>
          <Field
            label={<Trans id="post_thread.category">Select a category</Trans>}
            name="category"
            input={<Input />}
            error={(error) => (
              <CategoryValidationError error={error}>
                {({ message }) => <FieldError>{message}</FieldError>}
              </CategoryValidationError>
            )}
          />
          <Field
            label={<Trans id="post_thread.thread_title">Thread title</Trans>}
            name="title"
            input={<Input />}
            error={(error, value) => (
              <ThreadTitleValidationError
                error={error}
                value={value.trim().length}
                min={2}
                max={6}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ThreadTitleValidationError>
            )}
          />
          <Field
            label={
              <Trans id="post_thread.thread_message">Message contents</Trans>
            }
            name="body"
            input={<Editor />}
            error={(error, value) => (
              <ValidationError
                error={error}
                value={value.trim().length}
                min={2}
                max={200}
              >
                {({ message }) => <FieldError>{message}</FieldError>}
              </ValidationError>
            )}
          />
        </CardFormBody>
        <CardFooter>
          <FormFooter
            submitText={<Trans id="post_thread.submit">Post thread</Trans>}
          />
        </CardFooter>
      </Form>
    </Card>
  )
}

export default PostThreadForm
