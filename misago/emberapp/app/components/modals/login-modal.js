import Ember from 'ember';
import ModalComponent from 'misago/mixins/modal-component';

export default Ember.Component.extend(ModalComponent, {
  className: 'modal-sign-in',

  isSmall: true
});
