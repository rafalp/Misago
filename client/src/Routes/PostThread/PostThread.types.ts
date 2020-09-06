export interface ICategoryChoiceChild {
  id: string
  name: string
  icon: string
  color: string
  isClosed: boolean
  extra: Record<string, any>
}

export interface ICategoryChoice extends ICategoryChoiceChild {
  children: Array<ICategoryChoiceChild>
}
