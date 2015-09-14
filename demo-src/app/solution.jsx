'use strict';

const React = require('react');

const QuestionList = require('./question-list.jsx');

const Actions = require('./actions.js');
const Views = require('./views.js');

class Solution extends React.Component {
  reset() {
    this.props.dispatcher.dispatch({
      actionType: Actions.RESET_AND_SELECT_ANOTHER
    });
  }
  goBack() {
    this.props.dispatcher.dispatch({
      actionType: Actions.CHANGE_VIEW,
      view: Views.VIEW_OPTIMIZED_FORMULAS
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
            <h2>The Resulting Formula is used to Solve the Problem:</h2>
            <p>{this.props.solution.solutionFormula}</p>
          </div>
        </div>
        <footer className="flex-row padded">
          <button className="btn-prev" onClick={this.goBack.bind(this)}>Previous</button>
          <div className="instructions">The optimized formulas are converted into the formula above and used to solve the problem.</div>
          <button className="flex-right" onClick={this.reset.bind(this)}>Ask Another Problem</button>
        </footer>
      </div>
    );
  }
}

module.exports = Solution;
