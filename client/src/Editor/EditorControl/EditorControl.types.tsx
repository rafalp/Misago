import { EditorContextData } from "../EditorContext"

export interface EditorControl {
  name: string
  title: string
  icon: string
  component?: React.ComponentType<EditorControlProps>
  onClick?: (context: EditorContextData) => void
}

export interface EditorControlProps {
  context: EditorContextData
  name: string
  title: string
  icon: string
}
