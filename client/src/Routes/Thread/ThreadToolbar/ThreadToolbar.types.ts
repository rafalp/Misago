export interface IThreadToolbarProps {
  pagination: {
    page: number
    pages: number
    url: (page: number) => string
  }
}
