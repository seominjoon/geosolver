'use strict';

const React = require('react');

const QuestionList = require('./question-list.jsx');

const Actions = require('./actions.js');

class Solution extends React.Component {
  reset() {
    this.props.dispatcher.dispatch({
      actionType: Actions.RESET_AND_SELECT_ANOTHER
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
          <div className="formula-list-container padded">
            <h2>The Resulting Formula is used to Solve the Question:</h2>
            <pre>
              Some crazy formula.
            </pre>
          </div>
        </div>
        <footer className="flex-row padded">
          <div className="instructions">The optimized formulas are converted into the formula above and used to solve the question.</div>
          <button className="flex-right" onClick={this.reset.bind(this)}>Ask Another Question</button>
        </footer>
      </div>
    );
  }
}

module.exports = Solution;
