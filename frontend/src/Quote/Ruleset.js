class Ruleset {
  constructor(rules) {
    this.rules = rules || []
  }

  push(name, func) {
    this.rules.push({ name, func })
  }

  replace(name, func) {
    this.rules = this.rules.map((rule) => {
      if (rule.name === name) {
        return { name, func }
      } else {
        return rule
      }
    })
  }

  before(beforeName, name, func) {
    const rules = []
    this.rules.forEach((rule) => {
      rules.push({ name, func })
      if (rule.name === beforeName) {
        rules.push(rule)
      }
    })
    this.rules = rules
  }

  after(afterName, name, func) {
    const rules = []
    this.rules.forEach((rule) => {
      if (rule.name === afterName) {
        rules.push(rule)
      }
      rules.push({ name, func })
    })
    this.rules = rules
  }
}

export default Ruleset
