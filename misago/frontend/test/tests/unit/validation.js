(function (Misago) {
  'use strict';

  var service = getMisagoService('validate');

  QUnit.module("Validate");

  QUnit.test("service factory", function(assert) {
    var validate = service.factory();
    assert.ok(validate, "service factory has returned service instance.");
  });

  QUnit.test("validate data", function(assert) {
    var validate = service.factory();
    var controller = {
      username: m.prop(''),
      password: m.prop('ok!'),

      validation: {
        username: [Misago.validators.required()],
        password: [Misago.validators.required()]
      }
    };

    assert.deepEqual(
      validate(controller),
      {
        username: [
          "This field is required."
        ]
      },
      "validate() validated invalid form correctly.");

    controller.username('fullname');
    assert.equal(validate(controller), null,
      "valid form validation didn't return errors");
  });

  QUnit.test("required validator", function(assert) {
    assert.ok(Misago.validators.required('yup'),
      "non-empty string passed validation.");
    assert.ok(Misago.validators.required(' '),
      "empty string failed validation.");
  });
}(Misago.prototype));
