import assert from 'assert';
import Countdown from 'misago/utils/countdown';

describe('Countdown', function() {
  it("counts down and then executes callback", function(done) {
    const countdown = new Countdown(function() {
      assert.ok(true, "countdown has finished");
      done();
    }, 4);

    countdown.count();
    countdown.count();
    countdown.count();
    countdown.count();
  });
});