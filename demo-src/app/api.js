'use strict';

const superagent = require('superagent');
const Promise = require('promise');

const QuestionSolution = require('./solution.js');

function getJson(url) {
  return new Promise((resolve, reject) => {
    superagent.get(url).send().end((err, response) => {
      if (!err && response) {
        try {
          const parsedJson = JSON.parse(response.text);
          resolve(parsedJson);
        } catch(e) {
          reject(e);
        }
      } else {
        reject(err);
      }
    });
  });
}

module.exports = {
  fetchQuestions: () => {
    return getJson("assets/dirs.json").then((questionDirs) => {
      const promises = questionDirs.map((dir) => {
        return getJson(`assets/${encodeURIComponent(dir)}/question.json`).then((question) => {
          question.key = dir;
          return question;
        });
      });
      return Promise.all(promises);
    });
  },
  solveQuestion: (question) => {
    const start = Date.now();
    const questionBaseUrl = `assets/${question.key}/`;
    return Promise.all([
      getJson(`${questionBaseUrl}text_parse.json`),
      getJson(`${questionBaseUrl}diagram_parse.json`),
      getJson(`${questionBaseUrl}optimized.json`),
      getJson(`${questionBaseUrl}answer.json`)
    ]).then(solutionParts => {
      return new Promise(resolve => {
        setTimeout(
          () => {
            resolve(new QuestionSolution(question, ...solutionParts));
          },
          Math.max(0, Math.random() * 2000 - (Date.now() - start))
        );
      });
    });
  }
};
