import { yupResolver } from "@hookform/resolvers/yup"
import React from "react"
import {
  DeepPartial,
  ErrorOption,
  FieldName,
  FieldValues,
  FormProvider as HookFormProvider,
  UnpackNestedValue,
  useForm,
} from "react-hook-form"
import { FormContext } from "./FormContext"

interface OnSubmit<FormValues extends FieldValues = FieldValues> {
  data: FormValues
  event?: React.BaseSyntheticEvent<object, any, any>
  clearErrors(name?: FieldName<FieldValues> | FieldName<FieldValues>[]): void
  setError(name: FieldName<FieldValues>, error: ErrorOption): void
}

interface FormProps<FormValues> {
  children?: React.ReactNode
  className?: string
  defaultValues?: UnpackNestedValue<DeepPartial<FormValues>>
  disabled?: boolean
  id?: string
  onSubmit?: (args: OnSubmit<FormValues>) => void | Promise<void>
  validationMode?: "onSubmit" | "onBlur" | "onChange"
  validators?: any
}

const Form = <
  FormValues extends FieldValues = FieldValues,
  ValidationContext extends object = object
>(
  props: FormProps<FormValues>
): JSX.Element => {
  const {
    children,
    className,
    defaultValues,
    disabled,
    id,
    onSubmit,
    validationMode,
    validators,
  } = props
  const methods = useForm<FormValues, ValidationContext>({
    defaultValues,
    resolver: validators ? yupResolver(validators) : undefined,
    mode: validationMode || "onBlur",
  })

  return (
    <HookFormProvider {...methods}>
      <FormContext.Provider value={{ disabled, id }}>
        <form
          className={className}
          id={id}
          onSubmit={methods.handleSubmit((data, event) => {
            if (disabled) {
              event?.preventDefault()
              return
            }

            if (onSubmit) {
              onSubmit({
                data,
                event,
                clearErrors: methods.clearErrors,
                setError: methods.setError,
              })
            }
          })}
        >
          {children}
        </form>
      </FormContext.Provider>
    </HookFormProvider>
  )
}

export default Form
