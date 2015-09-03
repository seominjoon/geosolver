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
        </div>
        <footer className="flex-row padded">
          <div className="instructions">Select a question from those available above.</div>
          <button className="flex-right"
              onClick={this.solveSelectedQuestion.bind(this)}
              disabled={this.props.isSolving}>
            {this.props.isSolving ? 'Solving...' : 'Solve Question'}
          </button>
        </footer>
      </div>
    );
  }
}

module.exports = SelectQuestion;
