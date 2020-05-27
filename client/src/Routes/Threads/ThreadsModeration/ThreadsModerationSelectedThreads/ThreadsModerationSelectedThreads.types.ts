import { IThreadCategory } from "../../Threads.types"

export interface ISelectedThread {
  id: string
  title: string
  replies: number
  category: IThreadCategory
}
