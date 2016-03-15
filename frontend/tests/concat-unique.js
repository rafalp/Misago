import assert from 'assert';
import concatUnique from 'misago/utils/concat-unique';

describe('Concat Unique', function() {
  it("concats two different lists", function() {
    let a = [
     {id: 1},
     {id: 2}
    ];

    let b = [
     {id: 3}
    ];

    assert.deepEqual(concatUnique(a, b), [
     {id: 1},
     {id: 2},
     {id: 3}
    ], "different lists were concated correctly");
  });

  it("concats overlapping lists", function() {
    let a = [
     {id: 1},
     {id: 2}
    ];

    let b = [
     {id: 1},
     {id: 2},
     {id: 3}
    ];

    assert.deepEqual(concatUnique(a, b), [
     {id: 1},
     {id: 2},
     {id: 3}
    ], "overlapping lists were concated correctly");
  });
});