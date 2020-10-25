import { MockedProvider } from "@apollo/react-testing"
import { withKnobs, boolean, text } from "@storybook/addon-knobs"
import React from "react"
import * as Yup from "yup"
import { BodyScrollLockProvider } from "../../Context"
import Editor from "../../Editor"
import PostThreadCategoryInput from "../../Routes/PostThread/PostThreadCategoryInput"
import { ButtonPrimary } from "../Button"
import { Field, FieldError, Form } from "../Form"
import Input from "../Input"
import { categories } from "../Storybook"
import {
  CategoryValidationError,
  ThreadTitleValidationError,
  ValidationError,
} from "../ValidationError"
import PostingForm from "./PostingForm"
import PostingFormAlert from "./PostingFormAlert"
import PostingFormBody from "./PostingFormBody"
import PostingFormCollapsible from "./PostingFormCollapsible"
import PostingFormDialog from "./PostingFormDialog"
import PostingFormHeader from "./PostingFormHeader"

export default {
  title: "UI/PostingForm",
  decorators: [withKnobs],
}

interface IPostingFormValues {
  title: string
  category: string
  markup: string
}

const Boilerplate: React.FC = ({ children }) => {
  const [fullscreen, setFullscreen] = React.useState(false)
  const [minimized, setMinimized] = React.useState(false)

  const PostingFormSchema = Yup.object().shape({
    title: Yup.string()
      .required("value_error.thread_title.missing")
      .min(5, "value_error.any_str.min_length")
      .max(100, "value_error.any_str.max_length")
      .matches(/[a-zA-Z0-9]/, "value_error.thread_title"),
    category: Yup.string().required("value_error.missing"),
    markup: Yup.string()
      .required("value_error.missing")
      .min(5, "value_error.any_str.min_length"),
  })

  return (
    <BodyScrollLockProvider>
      <MockedProvider>
        <PostingForm
          fullscreen={fullscreen}
          minimized={minimized}
          show={boolean("Show", true)}
        >
          <PostingFormDialog>
            <Form<IPostingFormValues>
              defaultValues={{
                title: "",
                category: categories[0].children[0].id,
                markup: "",
              }}
              disabled={boolean("Loading", false)}
              validationSchema={PostingFormSchema}
              onSubmit={async ({ clearError }) => {
                clearError()
              }}
            >
              <PostingFormBody>
                <PostingFormHeader
                  fullscreen={fullscreen}
                  minimized={minimized}
                  setFullscreen={setFullscreen}
                  setMinimized={setMinimized}
                >
                  {text("Title", "Posting form")}
                </PostingFormHeader>
                <PostingFormCollapsible>
                  {boolean("Alert", false) && (
                    <PostingFormAlert>Lorem ipsum dolor met.</PostingFormAlert>
                  )}
                  {children}
                </PostingFormCollapsible>
              </PostingFormBody>
            </Form>
          </PostingFormDialog>
        </PostingForm>
      </MockedProvider>
    </BodyScrollLockProvider>
  )
}

export const StartThreadForm = () => (
  <Boilerplate>
    <div className="row">
      <div className="col-12 col-sm-6 col-md-7 mb-3">
        <Field
          label="Thread title"
          name="title"
          input={<Input placeholder="Thread title" responsive />}
          error={(error, value) => (
            <ThreadTitleValidationError
              error={error}
              value={value.trim().length}
              min={5}
              max={100}
            >
              {({ message }) => <FieldError>{message}</FieldError>}
            </ThreadTitleValidationError>
          )}
          labelReaderOnly
        />
      </div>
      <div className="col-12 col-sm-6 col-md-5 mb-3">
        <Field
          label="Thread category"
          name="category"
          input={
            <PostThreadCategoryInput
              choices={categories}
              validChoices={categories.map((category) => category.id)}
              responsive
            />
          }
          error={(error, value) => (
            <CategoryValidationError error={error}>
              {({ message }) => <FieldError>{message}</FieldError>}
            </CategoryValidationError>
          )}
          labelReaderOnly
        />
      </div>
    </div>
    <Field
      label="Message contents"
      name="markup"
      className="form-group-editor"
      input={<Editor submit={<ButtonPrimary text="Submit" small />} />}
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
      labelReaderOnly
    />
  </Boilerplate>
)

export const ReplyForm = () => (
  <Boilerplate>
    <Field
      label="Message contents"
      name="markup"
      className="form-group-editor"
      input={<Editor submit={<ButtonPrimary text="Submit" small />} />}
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
      labelReaderOnly
    />
  </Boilerplate>
)
