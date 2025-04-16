class Select {
  constructor() {
    this.element = document.createElement("div")
    
    document.body.appendChild(this.element);
  }

  show(target, query, choices) {
    console.log(target, query)
  }

  hide() {

  }
}

const selectSingleton = new Select()

export default selectSingleton