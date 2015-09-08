'use strict';

const React = require('react');

const QuestionList = require('./question-list.jsx');

const Actions = require('./actions');

class SelectQuestion extends React.Component {
  solveSelectedQuestion() {
    this.props.dispatcher.dispatch({
      actionType: Actions.SOLVE_QUESTION
    });
  }
  render() {
    return (
      <div className="flex-column flex-grow">
        <div className="flex-column flex-grow scrollable">
          <QuestionList
              questions={this.props.questions}
              dispatcher={this.props.dispatcher}
              selectedIndex={this.props.selectedIndex}
              selectedAnswerKey={this.props.solution ? this.props.solution.answer : undefined} />
          <div className="solve-button-container">
            <button
                onClick={this.solveSelectedQuestion.bind(this)}
                disabled={this.props.isSolving}>
              {this.props.isSolving ? 'Solving...' : 'Solve Question'}
            </button>
          </div>
        </div>
      </div>
    );
  }
}

module.exports = SelectQuestion;
