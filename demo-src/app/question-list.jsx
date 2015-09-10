'use strict';

const React = require('react');

const Question = require('./question.jsx');

const Actions = require('./actions');
const util = require('./util.js');

class ArrowIcon extends React.Component {
  render() {
    return (
      <svg viewBox="0 0 32 32" width="35" height="35">
        <path d="M23.129,16.001c0,0.475-0.182,0.951-0.545,1.312L9.498,30.4l-2.626-2.626l11.774-11.773L6.872,4.228l2.626-2.627 l13.086,13.088C22.947,15.05,23.129,15.525,23.129,16.001z" />
      </svg>
    );
  }
}

class QuestionList extends React.Component {
  constructor(props) {
    super(props);
    this.questionsCount = this.props.questions.length;
  }
  selectPreviousQuestion() {
    this.props.dispatcher.dispatch({
      actionType: Actions.CHANGED_QUESTION,
      selectedIndex: Math.max(0, --this.props.selectedIndex)
    });
  }
  selectNextQuestion() {
    this.props.dispatcher.dispatch({
      actionType: Actions.CHANGED_QUESTION,
      selectedIndex: Math.min(this.questionsCount - 1, ++this.props.selectedIndex)
    });
  }
  render() {
    const questions = this.props.questions.map((q, i) => {
      const isSelectedQuestion = this.props.selectedIndex === i;
      const selected = isSelectedQuestion ? this.props.selectedAnswerKey : undefined;
      const activeFormula = isSelectedQuestion ? this.props.activeFormula : undefined;
      return (
        <li key={q.key}>
          <Question questionKey={q.key}
              text={q.text}
              choices={q.choices}
              selected={selected}
              activeFormula={activeFormula}
              words={q.sentence_words}
              entityMap={this.props.entityMap}/>
        </li>
      );
    });

    const transformPercent = -1 * this.props.selectedIndex * 100;
    const transform = util.prefixed('transform', `translate3d(${transformPercent}%, 0, 0)`);

    const hasNext = this.props.selectedIndex < this.questionsCount - 1;
    const hasPrev = this.props.selectedIndex > 0;

    return (
      <div className="padded">
        <div className="question-list-container flex-row">
          <button className="btn-transparent prev-question"
              onClick={this.selectPreviousQuestion.bind(this)}
              disabled={!hasPrev}>
            <ArrowIcon />
          </button>
          <div className="question-list">
            <ul className="flex-row" style={transform}>{questions}</ul>
          </div>
          <button className="btn-transparent next-question"
              onClick={this.selectNextQuestion.bind(this)}
              disabled={!hasNext}>
            <ArrowIcon />
          </button>
        </div>
      </div>
    );
  }
}

module.exports = QuestionList;
