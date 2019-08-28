let assert = require('assert');
let should = require('chai').should();
let expect = require('chai').expect();
let supertest = require('supertest');

let api = supertest('http://localhost:8000');

describe('Player Comp Test', function() {
    it ('should return json with array of player stats', function(done) {
        api.get('/playercomp/')
        .set('Accept', 'application/x-www-form-urlencoded')
        .query({
            'player1': 'Tom Brady',
            'player2': 'Alex Smith',
            'year': 2009
        })
        .expect(200, done);
    })
});
