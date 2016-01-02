import assert from 'assert';
import * as validators from 'misago/utils/validators';

describe("Validator", function() {
  it("required validator", function() {
    assert.equal(validators.required()('yup'), undefined,
      "non-empty string passed validation.");
    assert.equal(
      validators.required()(' '), gettext("This field is required."),
      "empty string failed validation.");
  });

  it("email validator", function() {
    assert.equal(validators.email()('simple@email.com'), undefined,
      "simple e-mail passed validation.");
    assert.equal(validators.email()('si.mp.le@ema.il.com'), undefined,
      "dotted e-mail passed validation.");
    assert.equal(validators.email()('si-mp-le@ema-il.com'), undefined,
      "hyphenated e-mail passed validation.");
    assert.equal(validators.email()('si_mp_le@ema_il.com'), undefined,
      "underscored e-mail passed validation.");
    assert.equal(validators.email()('si+mp+le@email.com'), undefined,
      "plused e-mail passed validation.");
    assert.equal(validators.email('Nope!')('hh'), 'Nope!',
      "non-email errored with message providen.");
  });

  it("minLength validator", function() {
    assert.equal(validators.minLength(5)('yusss'), undefined,
      "string of required length passed validation.");
    assert.equal(
      validators.minLength(5)('nope'),
      "Ensure this value has at least 5 characters (it has 4).",
      "too short string failed validation.");
  });

  it("maxLength validator", function() {
    assert.equal(validators.maxLength(5)('yusss'), undefined,
      "string of required length passed validation.");
    assert.equal(
      validators.maxLength(5)('too long!'),
      "Ensure this value has at most 5 characters (it has 9).",
      "too long string failed validation.");
  });

  it("usernameMinLength validator", function() {
    var settings = {
      username_length_min: 4
    };

    assert.equal(
      validators.usernameMinLength(settings)('yusss'), undefined,
      "username of required length passed validation.");
    assert.equal(
      validators.usernameMinLength(settings)('no'),
      "Username must be at least 4 characters long.",
      "too short username failed validation.");
  });

  it("usernameMaxLength validator", function() {
    var settings = {
      username_length_max: 4
    };

    assert.equal(
      validators.usernameMaxLength(settings)('yuss'), undefined,
      "username of required length passed validation.");
    assert.equal(
      validators.usernameMaxLength(settings)('too long!'),
      "Username cannot be longer than 4 characters.",
      "too long username failed validation.");
  });

  it("username validator", function() {
    assert.equal(validators.usernameContent()('v4lid'), undefined,
      "valid username passed validation.");
    assert.equal(
      validators.usernameContent()('++++'),
      "Username can only contain latin alphabet letters and digits.",
      "invalid username failed validation.");
  });

  it("passwordMinLength validator", function() {
    var settings = {
      password_length_min: 4
    };

    assert.equal(
      validators.passwordMinLength(settings)('yusss'), undefined,
      "password of required length passed validation.");
    assert.equal(
      validators.passwordMinLength(settings)('no'),
      "Valid password must be at least 4 characters long.",
      "too short password failed validation.");
  });
});