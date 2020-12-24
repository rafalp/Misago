import { IEditorContextValues } from "../EditorContext"

export interface EditorControl {
  name: string
  title: string
  icon: string
  component?: React.ComponentType<EditorControlProps>
  onClick?: (context: IEditorContextValues) => void
}

export interface EditorControlProps {
  context: IEditorContextValues
  name: string
  title: string
  icon: string
}
