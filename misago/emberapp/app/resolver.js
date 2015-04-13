import Ember from 'ember';
import Resolver from 'ember/resolver';

export default Resolver.extend({
  _startsWith: function(string, beginning) {
    return string.indexOf(beginning) === 0;
  },

  _endsWith: function(string, tail) {
    return string.indexOf(tail, string.length - tail.length) !== -1;
  },

  misagoFormModuleName: function(parsedName) {
    if (this._endsWith(parsedName.name, '-form')) {
      var isComponent = parsedName.type === 'component';
      var isComponentTemplate = this._startsWith(parsedName.name, 'components/');

      if (isComponent || isComponentTemplate) {
        var path = parsedName.prefix + '/' +  this.pluralize(parsedName.type) + '/';

        if (isComponentTemplate) {
          path += 'components/forms/' + parsedName.fullNameWithoutType.substr(11);
        } else {
          path += 'forms/' + parsedName.fullNameWithoutType;
        }

        console.log(path);
        return path;
      }
    }
  },

  // register custom lookup
  moduleNameLookupPatterns: Ember.computed(function(){
    return Ember.A([
      this.misagoFormModuleName,
      this.podBasedModuleName,
      this.podBasedComponentsInSubdir,
      this.mainModuleName,
      this.defaultModuleName
    ]);
  })
});
