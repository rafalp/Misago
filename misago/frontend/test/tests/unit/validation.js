(function (Misago) {
  'use strict';

  var service = getMisagoService('validate');

  QUnit.module("Validate");

  QUnit.test("service factory", function(assert) {
    var validate = service.factory();
    assert.ok(validate, "service factory has returned service instance.");
  });

  QUnit.test("validate form", function(assert) {
    var validate = service.factory();
    var form = {
      username: m.prop(''),
      password: m.prop('ok!'),
      optional: m.prop(''),

      validation: {
        username: [],
        password: []
      }
    };

    assert.ok(!validate(form), "validate() returned false for invalid form.");

    assert.deepEqual(
      form.errors,
      {
        username: [
          "This field is required."
        ],
        password: true
      },
      "validate() set form.errors correctly.");

    form.username('fullname');
    assert.ok(validate(form), "validate() returned true for valid form.");

    assert.deepEqual(
      form.errors,
      {
        username: true,
        password: true
      },
      "valid form validation didn't return errors");
  });

  QUnit.test("validate field", function(assert) {
    var validate = service.factory();
    var form = {
      username: m.prop(''),

      validation: {
        username: []
      }
    };

    var validator = validate(form, 'username');
    validator('');

    assert.deepEqual(
      form.errors,
      {
        username: [
          "This field is required."
        ]
      },
      "field validator has set an error on form.");

    validator('fullname');

    assert.deepEqual(
      form.errors,
      {
        username: true
      },
      "field validator marked input as passing.");
  });

  QUnit.test("required validator", function(assert) {
    assert.equal(Misago.validators.required()('yup'), undefined,
      "non-empty string passed validation.");
    assert.equal(
      Misago.validators.required()(' '), gettext("This field is required."),
      "empty string failed validation.");
  });

  QUnit.test("email validator", function(assert) {
    assert.equal(Misago.validators.email()('simple@email.com'), undefined,
      "simple e-mail passed validation.");
    assert.equal(Misago.validators.email()('si.mp.le@ema.il.com'), undefined,
      "dotted e-mail passed validation.");
    assert.equal(Misago.validators.email()('si-mp-le@ema-il.com'), undefined,
      "hyphenated e-mail passed validation.");
    assert.equal(Misago.validators.email()('si_mp_le@ema_il.com'), undefined,
      "underscored e-mail passed validation.");
    assert.equal(Misago.validators.email()('si+mp+le@email.com'), undefined,
      "plused e-mail passed validation.");
    assert.equal(
      Misago.validators.email('Nope!')('hh'), 'Nope!',
      "non-email errored with message providen.");
  });

  QUnit.test("minLength validator", function(assert) {
    assert.equal(Misago.validators.minLength(5)('yusss'), undefined,
      "string of required length passed validation.");
    assert.equal(
      Misago.validators.minLength(5)('nope'),
      "Ensure this value has at least 5 characters (it has 4).",
      "too short string failed validation.");
  });

  QUnit.test("maxLength validator", function(assert) {
    assert.equal(Misago.validators.maxLength(5)('yusss'), undefined,
      "string of required length passed validation.");
    assert.equal(
      Misago.validators.maxLength(5)('too long!'),
      "Ensure this value has at most 5 characters (it has 9).",
      "too long string failed validation.");
  });

  QUnit.test("usernameMinLength validator", function(assert) {
    var settings = {
      username_length_min: 4
    };

    assert.equal(
      Misago.validators.usernameMinLength(settings)('yusss'), undefined,
      "username of required length passed validation.");
    assert.equal(
      Misago.validators.usernameMinLength(settings)('no'),
      "Username must be at least 4 characters long.",
      "too short username failed validation.");
  });

  QUnit.test("usernameMaxLength validator", function(assert) {
    var settings = {
      username_length_max: 4
    };

    assert.equal(
      Misago.validators.usernameMaxLength(settings)('yuss'), undefined,
      "username of required length passed validation.");
    assert.equal(
      Misago.validators.usernameMaxLength(settings)('too long!'),
      "Username cannot be longer than 4 characters.",
      "too long username failed validation.");
  });

  QUnit.test("username validator", function(assert) {
    assert.equal(Misago.validators.usernameContent()('v4lid'), undefined,
      "valid username passed validation.");
    assert.equal(
      Misago.validators.usernameContent()('++++'),
      "Username can only contain latin alphabet letters and digits.",
      "invalid username failed validation.");
  });

  QUnit.test("passwordMinLength validator", function(assert) {
    var settings = {
      password_length_min: 4
    };

    assert.equal(
      Misago.validators.passwordMinLength(settings)('yusss'), undefined,
      "password of required length passed validation.");
    assert.equal(
      Misago.validators.passwordMinLength(settings)('no'),
      "Valid password must be at least 4 characters long.",
      "too short password failed validation.");
  });
}(Misago.prototype));
