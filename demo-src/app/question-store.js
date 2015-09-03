'use strict';

const EventEmitter = require('events').EventEmitter;

const api = require('./api.js');
const Actions = require('./actions.js');
const Views = require('./views.js');

const CHANGE_EVENT = 'change';

class QuestionStore extends EventEmitter {
  constructor(dispatcher) {
    super();

    this.state = {
      questions: undefined,
      selectedIndex: 0,
      solution: undefined,
      activeFormula: undefined,
      isSolving: false,
      activeView: Views.SELECT_QUESTIONS
    };

    dispatcher.register(payload => {
      switch(payload.actionType) {
        case Actions.LOAD_QUESTIONS: {
          api.fetchQuestions().then(questions => {
            this.state.questions = questions;
            this.emitChange();
          });
          break;
        }
        case Actions.SOLVE_QUESTION: {
          const question = this.state.questions[this.state.selectedIndex];

          this.state.isSolving = true;
          this.emitChange();

          // TODO (codeviking): Figure out why this is getting lost in the inline function below
          const self = this;
          api.solveQuestion(question).then(solution => {
            if (solution.question === question) {
              self.state.isSolving = false;
              self.state.solution = solution;
              self.state.activeView = Views.VIEW_PARSED_FORMULAS;
              self.emitChange();
            }
          });
          break;
        }
        case Actions.CHANGED_QUESTION: {
          this.state.selectedIndex = payload.selectedIndex;
          this.state.isSolving = false;
          this.state.solution = undefined;
          this.state.activeFormula = undefined;
          this.state.activeView = Views.SELECT_QUESTIONS;
          this.emitChange();
          break;
        }
        case Actions.FORMULA_ACTIVE: {
          this.state.activeFormula = payload.formula;
          this.emitChange();
          break;
        }
        case Actions.FORMULA_INACTIVE: {
          this.state.activeFormula = undefined;
          this.emitChange();
          break;
        }
        case Actions.CHANGE_VIEW: {
          this.state.activeView = payload.view;
          this.emitChange();
          break;
        }
        case Actions.RESET_AND_SELECT_ANOTHER: {
          this.state.selectedIndex = (
            this.state.selectedIndex === this.state.questions.length - 1
              ? 0
              : ++this.state.selectedIndex
          );
          this.state.isSolving = false;
          this.state.solution = undefined;
          this.state.activeFormula = undefined;
          this.state.activeView = Views.SELECT_QUESTIONS;
          this.emitChange();
          break;
        }
      }
    });
  }
  emitChange() {
    this.emit(CHANGE_EVENT, this.state);
  }
  addChangeListener(fn) {
    this.addListener(CHANGE_EVENT, fn);
  }
  removeChangeListener(fn) {
    this.removeListener(CHANGE_EVENT, fn);
  }
}

QuestionStore.Events = {
  SOLVING: 0,
  SOLVED: 1
};

module.exports = QuestionStore;
